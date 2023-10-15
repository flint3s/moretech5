<link href="../../../../../AppData/Local/Temp/stylesheet.css" rel="stylesheet">
<script lang="ts" setup>

interface Props {
  icon: string
  address: string
  workload?: "Возможны очереди" | "Высокая загруженость"
  routeDistance: string
  routeTime: string
  hideRouteInfo?: boolean
}

const props = defineProps<Props>()

</script>

<template>
  <div class="option">
    <div style="width: 48px;">
      <n-avatar
          :src="props.icon"
          circle
          round
          style="width: 48px;height: 48px; aspect-ratio: 1"
      />
    </div>
    <n-thing style="padding: 0 20px;">
      <template #header>
        {{ props.address }}
      </template>
      <template v-if="!hideRouteInfo" #description>
        <div class="distance-block">
          <n-icon
              class="route-icon"
              size="25"
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