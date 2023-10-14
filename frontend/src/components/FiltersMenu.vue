<script setup lang="ts">
import ArrowLeft from "@components/icons/ArrowLeft.vue";
import {ref} from "vue";

const selectedDepartmentCriteria = ref<
    Array<
        "individual" |
        "privilege" |
        "legalEntity" |
        "prime" |
        "availableForDisabledPeople"
    >
>([])

const selectedServiceCriteria = ref<
    Array<
        "accountsAndCards" |
        "credits" |
        "investments" |
        "servicesForPensioners" |
        "transfers"
    >
>([])

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
                        <n-icon size="26">
                            <ArrowLeft/>
                        </n-icon>
                    </template>
                </n-button>
                <n-h2 style="margin: auto; color: var(--text-primary)">Фильтры</n-h2>
            </n-space>
            <n-space>
                <n-button
                    text
                    :focusable="false"
                    class="filter-button"
                    @click="() => {
                        selectedDepartmentCriteria = []
                        selectedServiceCriteria = []
                    }"
                >
                    Сбросить
                </n-button>
                <n-button
                    text
                    :focusable="false"
                    class="filter-button"
                >
                    Готово
                </n-button>
            </n-space>
        </div>
    </div>
    <n-thing class="filter-block">
        <template #footer>
            Фильтры отделений
        </template>
        <template #action>
            <n-space>
                <n-tag
                    round
                    checkable
                    :checked="selectedDepartmentCriteria.includes('individual')"
                    @update-checked="(value: boolean) => {
                        if (value)
                            selectedDepartmentCriteria.push('individual');
                        else
                            selectedDepartmentCriteria = selectedDepartmentCriteria.filter(v => v != 'individual')
                    }"
                    class="chip"
                    type="info"
                >
                    Физические лица
                </n-tag>
                <n-tag
                    bordered
                    round
                    checkable
                    :checked="selectedDepartmentCriteria.includes('privilege')"
                    @update-checked="(value: boolean) => {
                        if (value)
                            selectedDepartmentCriteria.push('privilege');
                        else
                            selectedDepartmentCriteria = selectedDepartmentCriteria.filter(v => v != 'privilege')
                        }"
                    class="chip"
                    type="info"
                >
                    Привилегия
                </n-tag>
                <n-tag
                    bordered
                    round
                    checkable
                    :checked="selectedDepartmentCriteria.includes('legalEntity')"
                    @update-checked="(value: boolean) => {
                      if (value)
                          selectedDepartmentCriteria.push('legalEntity');
                      else
                          selectedDepartmentCriteria = selectedDepartmentCriteria.filter(v => v != 'legalEntity')
                    }"
                    class="chip"
                    type="info"
                >
                    Юридические лица
                </n-tag>
                <n-tag
                    bordered
                    round
                    checkable
                    :checked="selectedDepartmentCriteria.includes('prime')"
                    @update-checked="(value: boolean) => {
                        if (value)
                            selectedDepartmentCriteria.push('prime');
                        else
                            selectedDepartmentCriteria = selectedDepartmentCriteria.filter(v => v != 'prime')
                        }"
                    class="chip"
                    type="info"
                >
                    Прайм
                </n-tag>
                <n-tag
                    bordered
                    round
                    checkable
                    :checked="selectedDepartmentCriteria.includes('availableForDisabledPeople')"
                    @update-checked="(value: boolean) => {
                        if (value)
                            selectedDepartmentCriteria.push('availableForDisabledPeople');
                        else
                            selectedDepartmentCriteria = selectedDepartmentCriteria.filter(v => v != 'availableForDisabledPeople')
                    }"
                    class="chip"
                    type="info"
                >
                    Доступно для маломобильных граждан
                </n-tag>
            </n-space>
        </template>
    </n-thing>
    <n-thing class="filter-block">
        <template #footer>
            Услуги
        </template>
        <template #action>
            <n-space>
                <n-tag
                    round
                    checkable
                    :checked="selectedServiceCriteria.includes('accountsAndCards')"
                    @update-checked="(value: boolean) => {
                        if (value)
                            selectedServiceCriteria.push('accountsAndCards');
                        else
                            selectedServiceCriteria = selectedServiceCriteria.filter(v => v != 'accountsAndCards')
                    }"
                    class="chip"
                    type="info"
                >
                    Банковские счета и карты
                </n-tag>
                <n-tag
                    bordered
                    round
                    checkable
                    :checked="selectedServiceCriteria.includes('credits')"
                    @update-checked="(value: boolean) => {
                        if (value)
                            selectedServiceCriteria.push('credits');
                        else
                            selectedServiceCriteria = selectedServiceCriteria.filter(v => v != 'credits')
                        }"
                    class="chip"
                    type="info"
                >
                    Кредиты и займы
                </n-tag>
                <n-tag
                    bordered
                    round
                    checkable
                    :checked="selectedServiceCriteria.includes('investments')"
                    @update-checked="(value: boolean) => {
                      if (value)
                          selectedServiceCriteria.push('investments');
                      else
                          selectedServiceCriteria = selectedServiceCriteria.filter(v => v != 'investments')
                    }"
                    class="chip"
                    type="info"
                >
                    Инвестиции и накопления
                </n-tag>
                <n-tag
                    bordered
                    round
                    checkable
                    :checked="selectedServiceCriteria.includes('servicesForPensioners')"
                    @update-checked="(value: boolean) => {
                        if (value)
                            selectedServiceCriteria.push('servicesForPensioners');
                        else
                            selectedServiceCriteria = selectedServiceCriteria.filter(v => v != 'servicesForPensioners')
                        }"
                    class="chip"
                    type="info"
                >
                    Банковские услуги для пенсионеров
                </n-tag>
                <n-tag
                    bordered
                    round
                    checkable
                    :checked="selectedServiceCriteria.includes('transfers')"
                    @update-checked="(value: boolean) => {
                        if (value)
                            selectedServiceCriteria.push('transfers');
                        else
                            selectedServiceCriteria = selectedServiceCriteria.filter(v => v != 'transfers')
                    }"
                    class="chip"
                    type="info"
                >
                    Переводы и платежи
                </n-tag>
            </n-space>
        </template>
    </n-thing>
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

.filter-block {
    margin-top: 8px;
    font-family: VTB Group UI Web Book, sans-serif;
    color: var(--light-text-color);
    padding: 6px;
}

.chip {
    border: 1px solid var(--n-color-checked);
    padding: 0 20px !important;
}

.chip:hover {
    border: 1px solid var(--accent-color-hover);
}

</style>