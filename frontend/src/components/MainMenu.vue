<script lang="ts" setup>
import DepartmentOption from "@components/DepartmentOption.vue";
import DirectionsWalkOutlined from "@components/icons/DirectionsWalkOutlined.vue";
import Search from "@components/icons/Search.vue";
import OptionsOutlined from "@components/icons/OptionsOutlined.vue";
import CarOutline from "@components/icons/CarOutline.vue";
import {defineEmits, ref, watchEffect} from "vue"
import {Department} from "@data/Department.ts";
import {Atm} from "@data/Atm.ts";

interface Props {
  departments: Department[],
  atms: Atm[],
  mode: 'departs' | 'atms' | 'search-departs',
  searchDepartments?: Department[],
  filters: any
}

defineProps<Props>()
const emit = defineEmits(['update:selectedDepartmentType', 'open-depart', 'to-filters', 'zoom-atm'])

const selectedDepartmentType = ref<"departs" | "atms">("departs")

const showDateTimePicker = ref<boolean>(false)
const selectedVisitTimeVariant = ref<"now" | "oneHourForward" | "other">("now")
const selectedTime = ref<number | undefined>()

const selectedRouteType = ref<'pedestrian' | 'driving'>("pedestrian")


watchEffect(() => {
  emit('update:selectedDepartmentType', selectedDepartmentType.value)
})
</script>

<template>
  <div class="flex-row">
    <n-input
        :bordered=false
        class="search-input"
        placeholder="Город, район, улица, метро"
    >
      <template #suffix>
        <n-icon>
          <Search/>
        </n-icon>
      </template>
    </n-input>
    <n-badge :show="!!filters.services.length || !!filters?.entity || filters.full_mobility || !!filters.feature" dot color="var(--accent-color)" :offset="[-8, 5]">
      <n-button
          :bordered=false
          :focusable="false"
          class="options-button"
          secondary
          @click="emit('to-filters')"
      >
        <template #icon>
          <n-icon>
            <OptionsOutlined/>
          </n-icon>
        </template>
      </n-button>
    </n-badge>
  </div>
  <n-thing class="filter-block">
    <template #action>
      <n-space>
        <n-tag
            :checked="selectedDepartmentType == 'departs'"
            checkable
            class="chip"
            round
            type="info"
            @update-checked="() => selectedDepartmentType = 'departs'"
        >
          Отделения
        </n-tag>
        <n-tag
            :checked="selectedDepartmentType == 'atms'"
            bordered
            checkable
            class="chip"
            round
            type="info"
            @update-checked="() => selectedDepartmentType = 'atms'"
        >
          Банкоматы
        </n-tag>
      </n-space>
    </template>
  </n-thing>
  <n-thing class="filter-block">
    <template #footer>
      Когда пойдёте в банк?
    </template>
    <template #action>
      <n-space>
        <n-tag
            :checked="selectedVisitTimeVariant == 'now'"
            checkable
            class="chip"
            round
            type="info"
            @update-checked="() => selectedVisitTimeVariant = 'now'"
        >
          Сейчас
        </n-tag>
        <n-tag
            :checked="selectedVisitTimeVariant == 'oneHourForward'"
            bordered
            checkable
            class="chip"
            round
            type="info"
            @update-checked="() => selectedVisitTimeVariant = 'oneHourForward'"
        >
          Через 1 час
        </n-tag>
        <n-popover
            :show="showDateTimePicker"
            trigger="click"
            @update-show="(value: boolean) => {
                            if (value || selectedTime == undefined) return

                            selectedVisitTimeVariant = 'now'
                        }"
        >
          <template #trigger>
            <n-tag
                :checked="selectedVisitTimeVariant == 'other'"
                bordered
                checkable
                class="chip"
                round
                @click="(value: boolean) => {
                                    selectedVisitTimeVariant = 'other';
                                    showDateTimePicker = value
                                }"
            >
              Другое время
            </n-tag>
          </template>
          <n-date-picker
              :default-value="new Date()"
              :value="selectedTime"
              panel
              type="datetime"
              value-format="dd.MM.yyyy"
              @confirm="() => {
                                showDateTimePicker = false;
                            }"
              @update-value="(value: number) =>{
                                selectedTime = value;
                            }"
          >

          </n-date-picker>
        </n-popover>
      </n-space>
    </template>
  </n-thing>
  <n-thing class="filter-block">
    <template #footer>
      Как будете добираться?
    </template>
    <template #action>
      <n-space>
        <n-tag
            :checked="selectedRouteType == 'pedestrian'"
            checkable
            class="chip"
            round
            @update-checked="() => selectedRouteType = 'pedestrian'"
        >
          <template #icon>
            <n-icon
                :class="selectedRouteType == 'pedestrian' ? 'checked-chip-icon' : 'chip-icon'"
            >
              <DirectionsWalkOutlined/>
            </n-icon>
          </template>
          Пешком
        </n-tag>
        <n-tag
            :checked="selectedRouteType == 'driving'"
            bordered
            checkable
            class="chip"
            round
            @update-checked="() => selectedRouteType = 'driving'"
        >
          <template #icon>
            <n-icon
                :class="selectedRouteType == 'driving' ? 'checked-chip-icon' : 'chip-icon'"
            >
              <CarOutline/>
            </n-icon>
          </template>
          На машине
        </n-tag>
      </n-space>
    </template>
  </n-thing>
  <n-thing v-if="mode === 'departs'" style="margin-top: 8px;">
    <template #footer>
                <span style="margin-left: 8px;">
                    Отделения поблизости
                </span>
    </template>
    <template #action>
      <n-scrollbar style="max-height: 55vh">
        <n-list
            :show-divider=false
            clickable
            hoverable
        >
          <n-list-item
              v-for="depart in departments"
              class="list-item"
          >
            <DepartmentOption
                :hide-route-info="!depart?.routeData"
                :address="depart.address"
                icon="https://telegra.ph/file/08190aa90245e99aed9ad.png"
                :route-distance="depart.routeData?.distance || ''"
                :route-time="depart.routeData?.duration || ''"
                @click="emit('open-depart', depart)"
            >
              <template #icon>
                <DirectionsWalkOutlined/>
              </template>
            </DepartmentOption>
          </n-list-item>
        </n-list>
      </n-scrollbar>
    </template>
  </n-thing>
  <n-thing v-else-if="mode === 'search-departs'" style="margin-top: 8px;">
    <template #footer>
                <span style="margin-left: 8px;">
                    Подходящие отделения
                </span>
    </template>
    <template #action>
      <n-scrollbar style="max-height: 55vh">
        <n-list
            :show-divider=false
            clickable
            hoverable
        >
          <n-list-item
              v-for="depart in searchDepartments"
              class="list-item"
          >
            <DepartmentOption
                :hide-route-info="!depart?.routeData"
                :address="depart.address"
                icon="https://telegra.ph/file/08190aa90245e99aed9ad.png"
                :route-distance="depart.routeData?.distance || ''"
                :route-time="depart.routeData?.duration || ''"
                @click="emit('open-depart', depart)"
            >
              <template #icon>
                <DirectionsWalkOutlined/>
              </template>
            </DepartmentOption>
          </n-list-item>
        </n-list>
      </n-scrollbar>
    </template>
  </n-thing>
  <n-thing v-else style="margin-top: 8px;">
    <template #footer>
                <span style="margin-left: 8px;">
                    Банкоматы поблизости
                </span>
    </template>
    <template #action>
      <n-scrollbar style="max-height: 55vh">
        <n-list
            :show-divider=false
            clickable
            hoverable
        >
          <n-list-item
              v-for="atm in atms"
              class="list-item"
          >
            <DepartmentOption
                hide-route-info
                :address="atm.address"
                icon="https://telegra.ph/file/08190aa90245e99aed9ad.png"
                route-distance="1,8 км"
                route-time="от 23 мин."
                @click="emit('zoom-atm', atm)"
            >
              <template #icon>
                <DirectionsWalkOutlined/>
              </template>
            </DepartmentOption>
          </n-list-item>
        </n-list>
      </n-scrollbar>
    </template>
  </n-thing>
</template>

<style scoped>
.flex-row {
  display: flex;
  align-items: center;
}

.filter-block {
  margin-top: 8px;
  font-family: VTB Group UI Web Book, sans-serif;
  color: var(--light-text-color);
  padding: 6px;
}

.chip {
  border: 1px solid var(--accent-color);
  padding: 0 20px !important;
}

.chip:hover {
  border: 1px solid var(--accent-color-hover);
}

.search-input, .options-button {
  text-align: left;
  border-radius: 12px;
  padding: 6px 10px;
  margin-right: 4px;
  font-size: 16px;
  height: 48px;
}

.options-button {
  width: 48px;
  margin-left: 10px;
}

.chip-icon {
  color: var(--accent-color);
}

.checked-chip-icon {
  color: #fff;
}

.options-button:hover {
  color: var(--accent-color);
}

.list-item, .list-item:hover {
  padding: 3px 6px !important;
  border-radius: 16px;
}

.list-item:hover {
  background: var(--inner-container-color);
}

span {
  font-family: VTB Group UI Web Book, sans-serif;
}
</style>