# 🔌 HobOS Device Driver Architecture (Phase 9)

## Hardware Abstractions
```
                  ┌──────────────────────┐
                  │ Virtual File System  │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Driver Device Table  │
                  └──────────┬───────────┘
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
     ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
     │ PL011 UART   │ │ GICv2 Ctrl   │ │ ARM Generic  │
     │ Driver       │ │ Driver       │ │ Timer Driver │
     └──────────────┘ └──────────────┘ └──────────────┘
```

