#include "device_memory.h"

#include <assert.h>
#include <stdio.h>

int main(void) {
    ExptMemoryTracker primary;
    uint32_t total = 0U;
    EXPT_InitMemoryTracker(&primary, 128U, 64U, 1);
    assert(EXPT_ReportProcessMemory(&primary, 1001U, 32U) == EXPT_OK);
    assert(EXPT_ReportProcessMemory(&primary, 1002U, 48U) == EXPT_OK);
    assert(EXPT_GetAmountOfMemUseInCpu(&primary, &total) == EXPT_OK);
    assert(total == 272U);
    assert(EXPT_RemoveProcessMemory(&primary, 1001U) == EXPT_OK);
    assert(EXPT_GetAmountOfMemUseInCpu(&primary, &total) == EXPT_OK);
    assert(total == 240U);

    ExptMemoryTracker secondary;
    EXPT_InitMemoryTracker(&secondary, 128U, 64U, 0);
    assert(EXPT_GetAmountOfMemUseInCpu(&secondary, &total) == EXPT_ERROR);
    assert(EXPT_RETRY_INTERVAL_SECONDS * EXPT_MAX_RETRIES == 300U);
    printf("PASS case 17: total=%u MB, exited process removed, primary-only guard enforced\n", total);
    return 0;
}

