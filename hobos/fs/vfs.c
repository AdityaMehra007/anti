/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * vfs.c - Virtual File System & File Descriptor Table
 */

#include <hobos/vfs.h>
#include <hobos/mm.h>
#include <hobos/kernel.h>
#include <hobos/sync.h>

static struct file_desc fd_table[MAX_FDS];
static spinlock_t vfs_lock = SPINLOCK_INIT;
static LIST_HEAD(vnode_root_list);

void vfs_init(void) {
    printk("[VFS] Initializing Virtual File System Layer...\n");
    init_list_head(&vnode_root_list);
    for (int i = 0; i < MAX_FDS; i++) {
        fd_table[i].in_use = false;
        fd_table[i].vnode = NULL;
        fd_table[i].offset = 0;
    }
}

struct vnode *vfs_create_file(const char *name, void *data, size_t size) {
    spin_lock(&vfs_lock);
    struct vnode *vn = (struct vnode *)kmalloc(sizeof(struct vnode));
    if (!vn) {
        spin_unlock(&vfs_lock);
        return NULL;
    }

    int i = 0;
    while (name && name[i] && i < VFS_MAX_NAME - 1) {
        vn->name[i] = name[i];
        i++;
    }
    vn->name[i] = '\0';

    vn->type = VNODE_TYPE_FILE;
    vn->size = size;
    vn->private_data = data;
    vn->ops = NULL;
    init_list_head(&vn->children);
    list_add_tail(&vn->sibling, &vnode_root_list);

    spin_unlock(&vfs_lock);
    return vn;
}

struct vnode *vfs_lookup(const char *path) {
    spin_lock(&vfs_lock);
    struct list_head *pos;
    list_for_each(pos, &vnode_root_list) {
        struct vnode *vn = list_entry(pos, struct vnode, sibling);
        int i = 0;
        bool match = true;
        while (path[i] && vn->name[i]) {
            if (path[i] != vn->name[i]) { match = false; break; }
            i++;
        }
        if (match && path[i] == '\0' && vn->name[i] == '\0') {
            spin_unlock(&vfs_lock);
            return vn;
        }
    }
    spin_unlock(&vfs_lock);
    return NULL;
}

int vfs_open(const char *path, int flags) {
    struct vnode *vn = vfs_lookup(path);
    if (!vn) return -1;

    spin_lock(&vfs_lock);
    for (int i = 3; i < MAX_FDS; i++) { /* 0, 1, 2 reserved for stdio */
        if (!fd_table[i].in_use) {
            fd_table[i].in_use = true;
            fd_table[i].vnode = vn;
            fd_table[i].offset = 0;
            fd_table[i].flags = flags;
            spin_unlock(&vfs_lock);
            return i;
        }
    }
    spin_unlock(&vfs_lock);
    return -1;
}

int vfs_close(int fd) {
    if (fd < 0 || fd >= MAX_FDS || !fd_table[fd].in_use) return -1;
    spin_lock(&vfs_lock);
    fd_table[fd].in_use = false;
    fd_table[fd].vnode = NULL;
    spin_unlock(&vfs_lock);
    return 0;
}

ssize_t vfs_read(int fd, void *buf, size_t count) {
    if (fd < 0 || fd >= MAX_FDS || !fd_table[fd].in_use) return -1;
    struct file_desc *desc = &fd_table[fd];
    struct vnode *vn = desc->vnode;

    if (desc->offset >= vn->size) return 0; /* EOF */

    size_t to_read = MIN(count, vn->size - desc->offset);
    char *src = (char *)vn->private_data + desc->offset;
    char *dst = (char *)buf;

    for (size_t i = 0; i < to_read; i++) {
        dst[i] = src[i];
    }

    desc->offset += to_read;
    return to_read;
}

ssize_t vfs_write(int fd, const void *buf, size_t count) {
    if (fd < 0 || fd >= MAX_FDS || !fd_table[fd].in_use) return -1;
    /* Basic read-only in-memory ramfs demonstration */
    return count;
}
