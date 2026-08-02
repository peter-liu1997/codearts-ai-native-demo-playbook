#ifndef DEVICE_MEMORY_H
#define DEVICE_MEMORY_H

#include <stddef.h>
#include <stdint.h>

#define EXPT_OK 0U
#define EXPT_ERROR 1U
#define EXPT_MAX_PROCESSES 64U
#define EXPT_RETRY_INTERVAL_SECONDS 1U
#define EXPT_MAX_RETRIES 300U

typedef struct {
    uint32_t process_id;
    uint32_t memory_mb;
    int active;
} ExptProcessMemory;

typedef struct {
    uint32_t rtos_base_mb;
    uint32_t service_base_mb;
    int is_primary;
    ExptProcessMemory processes[EXPT_MAX_PROCESSES];
} ExptMemoryTracker;

void EXPT_InitMemoryTracker(ExptMemoryTracker *tracker, uint32_t rtos_base_mb,
                            uint32_t service_base_mb, int is_primary);
uint32_t EXPT_ReportProcessMemory(ExptMemoryTracker *tracker, uint32_t process_id,
                                  uint32_t memory_mb);
uint32_t EXPT_RemoveProcessMemory(ExptMemoryTracker *tracker, uint32_t process_id);
uint32_t EXPT_GetAmountOfMemUseInCpu(const ExptMemoryTracker *tracker,
                                     uint32_t *mem_size_mb);

#endif

