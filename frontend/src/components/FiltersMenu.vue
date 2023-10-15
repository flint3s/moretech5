<script lang="ts" setup>
import ArrowLeft from "@components/icons/ArrowLeft.vue";
import {computed, ref} from "vue";

const emit = defineEmits(['back', "update:filters"])

const allServices = [
  "Открытие стандартного счёта ЛОРО",
  "Торговое финансирование",
  "Сделка «иностранная валюта/валюта РФ»",
  "Операции на межбанковском рынке",
  "Приём и выдача наличной валюты и российских рублей",
  "Приём ветхих и изымаемых банкнот на инкассо",
  "Размен/обмен иностранной валюты",
  "Покупка и продажа облигаций",
  "Операции РЕПО",
  "Выдача и оплата простых векселей ВТБ",
  "Покупка и продажа еврооблигаций",
  "Хранение простых векселей ВТБ",
  "Новация простых векселей ВТБ",
  "Заключение сделок опцион на облигации",
  "Заключение сделок форвард на акции",
  "Новация векселей ВТБ одного номинала на векселя другого",
  "Кредитование под залог векселей ВТБ",
  "Подтверждение факта выдачи простых векселей ВТБ",
  "Операции РЕПО с еврооблигациями",
  "Обезличенные металлические счета",
  "Операции с обезличенным драг. металлом",
  "Операции с физическим драг. металлом",
  "Привлечение межбанковских кредитов",
  "Открытие и ведение счетов депо",
  "Хранение и учёт прав на ценные бумаги",
  "Операции с ценными бумагами по счетам депо",
  "Фиксация обременения ценных бумаг",
  "Сопровождение корпоративных действий",
  "Изменение условия обременения ценных бумаг",
  "Открытие и ведение иных счетов",
  "Услуги, сопутствующие депозитарной деятельност",
  "Управление краткосрочной ликвидностью",
  "Размещение долгосрочной ликвидности",
  "Открыть счет",
  "Регистрация бизнеса",
  "Электронная подпись",
  "Подключить эквайринг",
  "Оформить кредит",
  "Онлайн-налог для АУСН",
  "Расчетный счет для бизнеса",
  "Оформить карту"
]

const props = defineProps<{filters: {
  coords: {
    latitude: number,
    longitude: number
  },
  entity: string,
  feature: string,
  full_mobility: boolean,
  services: string[]
}}>()

const _filters = reactive({
  coords: {
    latitude: 0,
    longitude: 0
  },
  entity: '',
  feature: '',
  full_mobility: false,
  services: [] as string[]
})

const clearFilters = () => {
  _filters.coords = {
    latitude: 0,
    longitude: 0
  }
  _filters.entity = ''
  _filters.feature = ''
  _filters.full_mobility = false
  _filters.services = [] as string[]
}

const servicesFilter = ref('')
const filteredServices = computed(() => {
  return allServices.filter(s => s.toLowerCase().includes(servicesFilter.value.toLowerCase()))
})

onMounted(() => {
  _filters.services = props.filters.services
  _filters.full_mobility = props.filters.full_mobility
  _filters.feature = props.filters.feature
  _filters.entity = props.filters.entity
})
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
            @click="clearFilters"
        >
          Сбросить
        </n-button>
        <n-button
            :focusable="false"
            class="filter-button"
            text
            @click="emit('update:filters', _filters)"
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
            :checked="_filters.entity === 'individual'"
            checkable
            class="chip"
            round
            type="info"
            @update-checked="(value: boolean) => {
                if (value)
                    _filters.entity = 'individual'
                else
                    _filters.entity = ''
            }"
        >
          Физические лица
        </n-tag>
        <n-tag
            :checked="_filters.feature === 'privilege'"
            bordered
            checkable
            class="chip"
            round
            type="info"
            @update-checked="(value: boolean) => {
                if (value)
                    _filters.feature = 'privilege'
                else
                    _filters.feature = ''
            }"
        >
          Привилегия
        </n-tag>
        <n-tag
            :checked="_filters.entity === 'legal'"
            bordered
            checkable
            class="chip"
            round
            type="info"
            @update-checked="(value: boolean) => {
              if (value)
                    _filters.entity = 'legal'
                else
                    _filters.entity = ''
            }"
        >
          Юридические лица
        </n-tag>
        <n-tag
            :checked="_filters.feature === 'prime'"
            bordered
            checkable
            class="chip"
            round
            type="info"
            @update-checked="(value: boolean) => {
              if (value)
                    _filters.feature = 'prime'
                else
                    _filters.feature = ''
            }"
        >
          Прайм
        </n-tag>
        <n-tag
            :checked="_filters.full_mobility"
            bordered
            checkable
            class="chip"
            round
            type="info"
            @update-checked="(value: boolean) => {
                _filters.full_mobility=value;
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
      <n-input placeholder="Поиск по услугам" class="mt-2" v-model:value="servicesFilter"/>
    </template>
    <template #action>
      <n-scrollbar style="max-height: 65vh">

        <n-space>
          <n-tag
              v-for="service in filteredServices"
              :checked="_filters.services.includes(service)"
              checkable
              class="chip"
              round
              style="white-space: break-spaces; height: 38px;"
              type="info"
              @update-checked="(value: boolean) => {
                if (value)
                    _filters.services.push(service);
                else
                    _filters.services = _filters.services.filter(v => v != service)
            }"
          >
            {{ service }}
          </n-tag>
        </n-space>
      </n-scrollbar>
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