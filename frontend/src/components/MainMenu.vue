<script setup lang="ts">
import DepartmentOption from "@components/DepartmentOption.vue";
import DirectionsWalkOutlined from "@components/icons/DirectionsWalkOutlined.vue";
import Search from "@components/icons/Search.vue";
import OptionsOutlined from "@components/icons/OptionsOutlined.vue";
import CarOutline from "@components/icons/CarOutline.vue";
import {ref, watchEffect, defineEmits} from "vue"

const emit = defineEmits(['update:selectedDepartmentType'])
const items = [1, 2, 3, 4, 5]

const selectedDepartmentType = ref<"departs" | "atms">("departs")

const selectedVisitTimeVariant = ref<"now" | "oneHourForward" | "other">("now")
//@ts-ignore
const selectedTime = ref<number | undefined>()

const selectedRouteType = ref<'pedestrian' | 'driving'>("pedestrian")


watchEffect(() => {
  emit('update:selectedDepartmentType', selectedDepartmentType.value)
})
</script>

<template>
    <div class="main-menu">
        <div class="flex-row">
            <n-input
                class="search-input"
                :bordered=false
                placeholder="Город, район, улица, метро"
            >
                <template #suffix>
                    <n-icon>
                        <Search/>
                    </n-icon>
                </template>
            </n-input>
            <n-button
                class="options-button"
                quaternary
                :bordered=false
            >
                <template #icon>
                    <OptionsOutlined/>
                </template>
            </n-button>
        </div>
        <n-thing class="filter-block">
            <template #action>
                <n-space>
                    <n-tag
                        round
                        checkable
                        :checked="selectedDepartmentType == 'departs'"
                        @checked-change="() => selectedDepartmentType = 'departs'"
                        class="chip"
                        type="info"
                    >
                        Отделения
                    </n-tag>
                    <n-tag
                        bordered
                        round
                        checkable
                        :checked="selectedDepartmentType == 'atms'"
                        @checked-change="() => selectedDepartmentType = 'atms'"
                        class="chip"
                        type="info"
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
                        round
                        checkable
                        :checked="selectedVisitTimeVariant == 'now'"
                        @checked-change="() => selectedVisitTimeVariant = 'now'"
                        class="chip"
                        type="info"
                    >
                        Сейчас
                    </n-tag>
                    <n-tag
                        bordered
                        round
                        checkable
                        :checked="selectedVisitTimeVariant == 'oneHourForward'"
                        @checked-change="() => selectedVisitTimeVariant = 'oneHourForward'"
                        class="chip"
                        type="info"
                    >
                        Через 1 час
                    </n-tag>
                    <n-tag
                        bordered
                        round
                        checkable
                        :checked="selectedVisitTimeVariant == 'other'"
                        @checked-change="() =>{
                            selectedVisitTimeVariant = 'other';
                        }"
                        class="chip"
                        type="info"
                    >
                        Другое время
                    </n-tag>
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
                        round
                        checkable
                        class="chip"
                        :checked="selectedRouteType == 'pedestrian'"
                        @checked-change="() => selectedRouteType = 'pedestrian'"
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
                        bordered
                        round
                        checkable
                        class="chip"
                        :checked="selectedRouteType == 'driving'"
                        @checked-change="() => selectedRouteType = 'driving'"
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
        <n-thing style="margin-top: 8px;">
            <template #footer>
                <span style="margin-left: 8px;">
                    Отделения поблизости
                </span>
            </template>
            <template #action>
                <n-list
                    hoverable
                    clickable
                    :show-divider=false
                >
                    <n-list-item
                        class="list-item"
                        v-for="_ in items"
                    >
                        <DepartmentOption
                            address="ул. Залупинская, д. 22"
                            route-distance="1,8 км"
                            icon="https://sun9-53.userapi.com/impg/hh8KgHsQ2ahxXqLPlEn_6fMwv4L-24OdtQQtZg/-ZOhX3i7pXw.jpg?size=1024x1024&quality=95&sign=71a7f9116f3a3f4de8d09b0679c6f520&type=album"
                            route-time="от 23 мин.">
                            <template #icon>
                                <DirectionsWalkOutlined/>
                            </template>
                        </DepartmentOption>
                    </n-list-item>
                </n-list>
            </template>
        </n-thing>
    </div>
</template>

<style scoped>
.main-menu {
    padding: 20px 12px;
    background: var(--container-color);
    border-radius: 16px;
    width: 400px;
    text-align: left;
}

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
    background: var(--inner-container-color);
    text-align: left;
    border-radius: 12px;
    padding: 6px 10px;
    margin-right: 4px;
    font-size: 16px;
    height: 48px;
}

.options-button {
    width: 48px;
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