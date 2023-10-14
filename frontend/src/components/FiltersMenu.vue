<script setup lang="ts">

import ArrowLeft from "@components/icons/ArrowLeft.vue";
</script>

<template>
    <div class="filter-menu">
        <div class="filter-header">
            <n-space class="flex-v-center">
                <n-button
                    round
                    text
                    :focusable="false"
                    class="back-button-icon"
                >
                    <template #icon>
                        <n-icon>
                            <ArrowLeft/>
                        </n-icon>
                    </template>
                </n-button>
                <n-h2>Фильтры</n-h2>
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
.filter-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.filter-button {
    color: var(--accent-color);
}

.back-button-icon {
    width: 36px;
    height: 36px;
}

.back-button-icon:hover {
    color: var(--accent-color);
}

.flex-v-center {
    display: flex;
    align-items: center;
}

</style>