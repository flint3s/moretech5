<template>
  <n-config-provider
      :date-locale="dateRuRU"
      :locale="ruRU"
  >
    <n-dialog-provider>
      <n-message-provider>
        <transition mode="out-in" name="fade">
          <router-view v-slot="{ Component }">
            <component :is="Component"/>
          </router-view>
        </transition>
      </n-message-provider>
    </n-dialog-provider>
  </n-config-provider>
</template>

<script lang="ts" setup>
import {dateRuRU, ruRU} from "naive-ui";
</script>