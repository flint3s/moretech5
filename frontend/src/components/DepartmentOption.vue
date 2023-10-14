<link rel="stylesheet" href="../../../../../AppData/Local/Temp/stylesheet.css">
<script setup lang="ts">

interface Props {
    icon: string
    address: string
    workload?: "Возможны очереди" | "Высокая загруженость"
    routeDistance: string
    routeTime: string
}

const props = defineProps<Props>()

</script>

<template>
    <div class="option">
        <n-avatar
            round
            :src=props.icon
            style="width: 48px;height: 48px;"
        />
        <n-thing style="padding: 0 20px;">
            <template #header>
                {{ props.address }}
            </template>
            <template #description>
                <div class="distance-block">
                    <n-icon
                        size="25"
                        class="route-icon"
                        style="padding: 0; margin-left: -5px; margin-right: 10px;"
                    >
                        <slot name="icon"/>
                    </n-icon>
                    {{ props.routeDistance }} ·
                    <n-text class="route-time-text">
                        {{ props.routeTime }}
                    </n-text>
                </div>
            </template>
        </n-thing>
    </div>
</template>

<style scoped>
.route-time-text {
    color: var(--accent-color);
}

.option, .distance-block {
    display: flex;
    align-items: center;
    font-family: VTB Group UI Web Book, sans-serif;
}

.distance-block * {
    padding: 0 5px;
}

.route-icon {
    margin-left: -5px;
    margin-right: 10px;
}
</style>