#include "device_memory.h"

#include <string.h>

void EXPT_InitMemoryTracker(ExptMemoryTracker *tracker, uint32_t rtos_base_mb,
                            uint32_t service_base_mb, int is_primary) {
    if (tracker == NULL) return;
    memset(tracker, 0, sizeof(*tracker));
    tracker->rtos_base_mb = rtos_base_mb;
    tracker->service_base_mb = service_base_mb;
    tracker->is_primary = is_primary;
}

uint32_t EXPT_ReportProcessMemory(ExptMemoryTracker *tracker, uint32_t process_id,
                                  uint32_t memory_mb) {
    size_t free_slot = EXPT_MAX_PROCESSES;
    if (tracker == NULL || process_id == 0U) return EXPT_ERROR;
    for (size_t index = 0; index < EXPT_MAX_PROCESSES; ++index) {
        ExptProcessMemory *row = &tracker->processes[index];
        if (row->active && row->process_id == process_id) {
            row->memory_mb = memory_mb;
            return EXPT_OK;
        }
        if (!row->active && free_slot == EXPT_MAX_PROCESSES) free_slot = index;
    }
    if (free_slot == EXPT_MAX_PROCESSES) return EXPT_ERROR;
    tracker->processes[free_slot] = (ExptProcessMemory){process_id, memory_mb, 1};
    return EXPT_OK;
}

uint32_t EXPT_RemoveProcessMemory(ExptMemoryTracker *tracker, uint32_t process_id) {
    if (tracker == NULL) return EXPT_ERROR;
    for (size_t index = 0; index < EXPT_MAX_PROCESSES; ++index) {
        ExptProcessMemory *row = &tracker->processes[index];
        if (row->active && row->process_id == process_id) {
            *row = (ExptProcessMemory){0U, 0U, 0};
            return EXPT_OK;
        }
    }
    return EXPT_ERROR;
}

uint32_t EXPT_GetAmountOfMemUseInCpu(const ExptMemoryTracker *tracker,
                                     uint32_t *mem_size_mb) {
    if (tracker == NULL || mem_size_mb == NULL || !tracker->is_primary) return EXPT_ERROR;
    uint64_t total = (uint64_t)tracker->rtos_base_mb + tracker->service_base_mb;
    for (size_t index = 0; index < EXPT_MAX_PROCESSES; ++index) {
        if (tracker->processes[index].active) total += tracker->processes[index].memory_mb;
    }
    if (total > UINT32_MAX) return EXPT_ERROR;
    *mem_size_mb = (uint32_t)total;
    return EXPT_OK;
}

