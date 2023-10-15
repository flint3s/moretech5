<script lang="ts" setup>
import ArrowLeft from "@components/icons/ArrowLeft.vue";
import {ref} from "vue";

const emit = defineEmits(['back'])

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
            :focusable="false"
            class="back-button-icon"
            round
            text
            @click="emit('back')"
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
            :focusable="false"
            class="filter-button"
            text
            @click="() => {
                        selectedDepartmentCriteria = []
                        selectedServiceCriteria = []
                    }"
        >
          Сбросить
        </n-button>
        <n-button
            :focusable="false"
            class="filter-button"
            text
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
            :checked="selectedDepartmentCriteria.includes('individual')"
            checkable
            class="chip"
            round
            type="info"
            @update-checked="(value: boolean) => {
                        if (value)
                            selectedDepartmentCriteria.push('individual');
                        else
                            selectedDepartmentCriteria = selectedDepartmentCriteria.filter(v => v != 'individual')
                    }"
        >
          Физические лица
        </n-tag>
        <n-tag
            :checked="selectedDepartmentCriteria.includes('privilege')"
            bordered
            checkable
            class="chip"
            round
            type="info"
            @update-checked="(value: boolean) => {
                        if (value)
                            selectedDepartmentCriteria.push('privilege');
                        else
                            selectedDepartmentCriteria = selectedDepartmentCriteria.filter(v => v != 'privilege')
                        }"
        >
          Привилегия
        </n-tag>
        <n-tag
            :checked="selectedDepartmentCriteria.includes('legalEntity')"
            bordered
            checkable
            class="chip"
            round
            type="info"
            @update-checked="(value: boolean) => {
                      if (value)
                          selectedDepartmentCriteria.push('legalEntity');
                      else
                          selectedDepartmentCriteria = selectedDepartmentCriteria.filter(v => v != 'legalEntity')
                    }"
        >
          Юридические лица
        </n-tag>
        <n-tag
            :checked="selectedDepartmentCriteria.includes('prime')"
            bordered
            checkable
            class="chip"
            round
            type="info"
            @update-checked="(value: boolean) => {
                        if (value)
                            selectedDepartmentCriteria.push('prime');
                        else
                            selectedDepartmentCriteria = selectedDepartmentCriteria.filter(v => v != 'prime')
                        }"
        >
          Прайм
        </n-tag>
        <n-tag
            :checked="selectedDepartmentCriteria.includes('availableForDisabledPeople')"
            bordered
            checkable
            class="chip"
            round
            type="info"
            @update-checked="(value: boolean) => {
                        if (value)
                            selectedDepartmentCriteria.push('availableForDisabledPeople');
                        else
                            selectedDepartmentCriteria = selectedDepartmentCriteria.filter(v => v != 'availableForDisabledPeople')
                    }"
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
            :checked="selectedServiceCriteria.includes('accountsAndCards')"
            checkable
            class="chip"
            round
            type="info"
            @update-checked="(value: boolean) => {
                        if (value)
                            selectedServiceCriteria.push('accountsAndCards');
                        else
                            selectedServiceCriteria = selectedServiceCriteria.filter(v => v != 'accountsAndCards')
                    }"
        >
          Банковские счета и карты
        </n-tag>
        <n-tag
            :checked="selectedServiceCriteria.includes('credits')"
            bordered
            checkable
            class="chip"
            round
            type="info"
            @update-checked="(value: boolean) => {
                        if (value)
                            selectedServiceCriteria.push('credits');
                        else
                            selectedServiceCriteria = selectedServiceCriteria.filter(v => v != 'credits')
                        }"
        >
          Кредиты и займы
        </n-tag>
        <n-tag
            :checked="selectedServiceCriteria.includes('investments')"
            bordered
            checkable
            class="chip"
            round
            type="info"
            @update-checked="(value: boolean) => {
                      if (value)
                          selectedServiceCriteria.push('investments');
                      else
                          selectedServiceCriteria = selectedServiceCriteria.filter(v => v != 'investments')
                    }"
        >
          Инвестиции и накопления
        </n-tag>
        <n-tag
            :checked="selectedServiceCriteria.includes('servicesForPensioners')"
            bordered
            checkable
            class="chip"
            round
            type="info"
            @update-checked="(value: boolean) => {
                        if (value)
                            selectedServiceCriteria.push('servicesForPensioners');
                        else
                            selectedServiceCriteria = selectedServiceCriteria.filter(v => v != 'servicesForPensioners')
                        }"
        >
          Банковские услуги для пенсионеров
        </n-tag>
        <n-tag
            :checked="selectedServiceCriteria.includes('transfers')"
            bordered
            checkable
            class="chip"
            round
            type="info"
            @update-checked="(value: boolean) => {
                        if (value)
                            selectedServiceCriteria.push('transfers');
                        else
                            selectedServiceCriteria = selectedServiceCriteria.filter(v => v != 'transfers')
                    }"
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
  border: 1px solid var(--accent-color);
  padding: 0 20px !important;
}

.chip:hover {
  border: 1px solid var(--accent-color-hover);
}

</style>