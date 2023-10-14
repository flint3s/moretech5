<template>
  <n-config-provider
      :date-locale="dateRuRU"
      :locale="ruRU"
      :theme="appTheme"
      :theme-overrides="themeOverrides"
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
import {darkTheme, dateRuRU, lightTheme, ruRU} from "naive-ui";
import themeOverrides from "@/app/naive-ui-theme-overrides.json";
import {useRootStore} from "@/store/rootStore.ts";

const rootStore = useRootStore();
rootStore.initTheme()

const appTheme = computed(() => {
  return rootStore.theme === 'light' ? lightTheme : darkTheme
})
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