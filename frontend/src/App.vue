<template>
  <n-config-provider
      :date-locale="dateRuRU"
      :locale="ruRU"
  >
    <n-dialog-provider>
      <n-message-provider>
        <router-view v-slot="{ Component }">
          <transition mode="out-in" name="fade">
            <component :is="Component"/>
          </transition>
        </router-view>
      </n-message-provider>
    </n-dialog-provider>
  </n-config-provider>
</template>

<script lang="ts" setup>
import {dateRuRU, ruRU} from "naive-ui";
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
}

:root {
  --accent-blue: #0D69F2;
}
</style>