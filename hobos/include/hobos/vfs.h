/*
 * HobOS - High-Performance ARM64 Educational & Research Operating System
 * vfs.h - Virtual File System interface and in-memory nodes
 */

#ifndef _HOBOS_VFS_H_
#define _HOBOS_VFS_H_

#include <hobos/types.h>
#include <hobos/list.h>

#define VFS_MAX_NAME 64
#define VFS_MAX_PATH 256
#define MAX_FDS      32

typedef enum {
    VNODE_TYPE_FILE,
    VNODE_TYPE_DIR,
    VNODE_TYPE_DEVICE
} vnode_type_t;

struct vnode;

struct vfs_ops {
    int (*open)(struct vnode *vn, int flags);
    int (*close)(struct vnode *vn);
    ssize_t (*read)(struct vnode *vn, void *buf, size_t count, size_t offset);
    ssize_t (*write)(struct vnode *vn, const void *buf, size_t count, size_t offset);
};

struct vnode {
    char name[VFS_MAX_NAME];
    vnode_type_t type;
    size_t size;
    struct vfs_ops *ops;
    void *private_data;
    struct list_head children;
    struct list_head sibling;
};

struct file_desc {
    struct vnode *vnode;
    size_t offset;
    int flags;
    bool in_use;
};

void vfs_init(void);
struct vnode *vfs_create_file(const char *name, void *data, size_t size);
struct vnode *vfs_lookup(const char *path);
int vfs_open(const char *path, int flags);
int vfs_close(int fd);
ssize_t vfs_read(int fd, void *buf, size_t count);
ssize_t vfs_write(int fd, const void *buf, size_t count);

#endif /* _HOBOS_VFS_H_ */
