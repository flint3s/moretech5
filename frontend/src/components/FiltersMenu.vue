<script setup lang="ts">

import ArrowLeft from "@components/icons/ArrowLeft.vue";
</script>

<template>
    <div class="filter-menu">
        <div class="filter-header">
            <n-space>
                <n-button
                    quaternary
                    :focusable="false"
                >
                    <template #icon>
                        <n-icon size="24">
                            <ArrowLeft/>
                        </n-icon>
                    </template>
                </n-button>
            </n-space>
            <n-space>
                <n-button
                    quaternary
                    :focusable="false"
                    class="filter-button"
                >
                    Сбросить
                </n-button>
                <n-button
                    quaternary
                    :focusable="false"
                    class="filter-button"
                >
                    Готово
                </n-button>
            </n-space>
        </div>
    </div>
</template>

<style scoped>
.filter-menu {
    padding: 20px 12px;
    width: 400px;
    background: var(--container-color);
}

.filter-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.filter-button {
    color: var(--accent-color);
}

</style>