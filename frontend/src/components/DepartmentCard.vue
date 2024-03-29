<template>
    <div>
        <div style="display:flex; align-items: center; gap: 12px">
            <n-button :focusable="false" text @click="emit('back')">
                <template #icon>
                    <n-icon>
                        <svg fill="none" height="16" viewBox="0 0 16 16" width="16" xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M3.8248 9.00005L8.7248 13.9C8.9248 14.1 9.02064 14.3334 9.01231 14.6C9.00397 14.8667 8.89981 15.1 8.69981 15.3C8.49981 15.4834 8.26647 15.5792 7.9998 15.5875C7.73314 15.5959 7.4998 15.5 7.2998 15.3L0.699805 8.70005C0.599805 8.60005 0.528971 8.49172 0.487305 8.37505C0.445638 8.25838 0.424805 8.13338 0.424805 8.00005C0.424805 7.86672 0.445638 7.74172 0.487305 7.62505C0.528971 7.50838 0.599805 7.40005 0.699805 7.30005L7.2998 0.700049C7.48314 0.516715 7.7123 0.425049 7.9873 0.425049C8.2623 0.425049 8.49981 0.516715 8.69981 0.700049C8.89981 0.900049 8.9998 1.13755 8.9998 1.41255C8.9998 1.68755 8.89981 1.92505 8.69981 2.12505L3.8248 7.00005H14.9998C15.2831 7.00005 15.5206 7.09588 15.7123 7.28755C15.904 7.47922 15.9998 7.71672 15.9998 8.00005C15.9998 8.28338 15.904 8.52088 15.7123 8.71255C15.5206 8.90422 15.2831 9.00005 14.9998 9.00005H3.8248Z"
                                fill="#0D69F2"/>
                        </svg>
                    </n-icon>
                </template>
            </n-button>

            <h2 style="font-size: 18px; line-height: 1.1;">
                {{ department.salePointName }}
            </h2>
        </div>

        <h4 style="margin-top: 12px; font-weight: normal; cursor: pointer;" @click="onClickCopyAddress">
            {{ department.address }}
        </h4>

        <h3 style="font-weight: normal" :class="{0: 'low', 1: 'medium', 2: 'high'}[department.fullness!]" v-if="[0, 1, 2].includes(department.fullness!)">
            {{departmentFullness}}
        </h3>

        <div v-if="isGeolocationAvailable">
            <h5 style="font-weight: normal">
                Как будете добираться?
            </h5>

            <n-spin :show="routesInfo.loading">
                <div style="display:flex; gap: 8px">
                    <div :class="{'active': selectedTransportType === 'pedestrian'}" class="transport-type-card"
                         @click="selectedTransportType = 'pedestrian'">
                        <PersonWalkIcon style="color: currentColor"/>
                        <span>Пешком</span>
                        <span>~{{ routesInfo.pedestrian.duration?.text || '...' }}</span>
                    </div>
                    <div :class="{'active': selectedTransportType === 'driving'}" class="transport-type-card"
                         @click="selectedTransportType = 'driving'">
                        <CarDrivingIcon/>
                        <span>На машине</span>
                        <span>~{{ routesInfo.driving.duration?.text || '...' }}</span>
                    </div>
                </div>

                <n-button block size="large" style="margin-top: 16px;" type="primary" @click="emit('build-route')">
                    Проложить маршрут · {{ routesInfo[selectedTransportType]?.distance?.text }}
                </n-button>
            </n-spin>
        </div>
        <n-alert v-else type="warning" title="Нет доступа к геолокации" show-icon>
          Включите геолокацию чтобы построить маршрут до отделения
        </n-alert>

        <div>
            <h5 class="fw-normal" style="font-size: 14px">Об отделении</h5>

            <div>
                <div class="d-flex align-items-center gap-3 mb-3">
                    <n-icon size="30">
                        <PremiumBankIcon/>
                    </n-icon>

                    <div>
                        <h4 class="fw-normal mb-1 mt-0 lh-1" style="font-size: 16px">Физические лица</h4>
                        <p class="fw-normal m-0 p-0">Все клиенты банка</p>
                    </div>
                </div>

                <div class="d-flex align-items-center gap-3 mb-3">
                    <n-icon size="30">
                        <PersonIcon/>
                    </n-icon>

                    <div>
                        <h4 class="fw-normal mb-1 mt-0 lh-1" style="font-size: 16px">Юридические лица</h4>
                        <p class="fw-normal m-0 p-0">Обслуживание банкосвких счетов организаций</p>
                    </div>
                </div>

                <div class="d-flex align-items-center gap-3 mb-3">
                    <n-icon size="30">
                        <TwoPersonsIcon/>
                    </n-icon>

                    <div>
                        <h4 class="fw-normal mb-1 mt-0 lh-1" style="font-size: 16px">Привилегия</h4>
                        <p class="fw-normal m-0 p-0">Текст</p>
                    </div>
                </div>

                <div class="d-flex align-items-center gap-3 mb-3">
                    <n-icon size="30">
                        <SofaIcon/>
                    </n-icon>

                    <div>
                        <h4 class="fw-normal mb-1 mt-0 lh-1" style="font-size: 16px">Зона премиального обслуживания</h4>
                        <p class="fw-normal m-0 p-0">Клиенты с пакетом «Привилегия»</p>
                    </div>
                </div>
            </div>
        </div>

        <div style="width: 100%;">
            <h5 class="fw-normal" style="margin-bottom: 4px; font-size: 14px">Посещаемость</h5>

            <n-radio-group v-model:value="selectedDayOfWeek" style="width: 100%;">
                <n-radio-button
                    style="width: calc(100% / 7); text-align: center"
                    v-for="dayOfWeek in daysOfWeek"
                    :key="dayOfWeek.value"
                    :value="dayOfWeek.value"
                    :label="dayOfWeek.label"
                />
            </n-radio-group>

            <apexchart
                type="bar"
                :series="[{
                    data: hours
                }]"
                :options="{
                    chart: {
                        toolbar: false,
                        selection: false,
                        width: '104%'
                    },
                    fill: {
                        colors: ['var(--accent-color)']
                    },
                    plotOptions: {
                        bar: {
                            columnWidth: '75%',
                            distributed: true,
                            colors: {
                                backgroundBarRadius: 8
                            }
                        }
                    },
                    stroke: {
                        show: false,
                    },
                    dataLabels: {
                        enabled: false
                    },
                    legend: {
                        show: false
                    },
                    labels: {
                        style: {
                            fontSize: '12px'
                        }
                    },
                    xaxis: {
                        categories: hours.map((e: number) => `${e < 10 ? '0' : ''}${e}:00`),
                        tickAmount: 5,
                        labels: {
                            rotate: 0,

                            style: {
                                fontFamily: 'VTB Group UI Web Book, sans-serif',
                                color: ['var(--text-primary)']
                            }
                        },
                        axisBorder: {
                            show: false
                        },
                        axisTicks: {
                            show: false
                        }
                    },
                    yaxis: {
                        show: false,
                    },
                    tooltip: {
                        enabled: false
                    },
                    grid: {
                        show: false
                    }
                }"
            />

        </div>
    </div>
</template>

<script lang="ts" setup>
import {Department as DepartmentType} from "@data/Department.ts";
import PersonWalkIcon from "@components/icons/PersonWalkIcon.vue";
import CarDrivingIcon from "@components/icons/CarDrivingIcon.vue";
import PremiumBankIcon from "@components/icons/PremiumBankIcon.vue";
import SofaIcon from "@components/icons/SofaIcon.vue";
import TwoPersonsIcon from "@components/icons/TwoPersonsIcon.vue";
import PersonIcon from "@components/icons/PersonIcon.vue";
import {reactive, ref, watchEffect} from "vue";
import {getRouteData} from "@data/computeRoute.ts";
import {axiosInstance} from "@/api/axiosInstance.ts";

interface Props {
    department: DepartmentType,
    currentUserPosition?: number[],
  isGeolocationAvailable: boolean
}

const props = defineProps<Props>()
const emit = defineEmits(['back', 'build-route'])
const message = useMessage()

const onClickCopyAddress = () => {
    navigator.clipboard.writeText(props.department.address)
    message.info('Адрес скопирован')
}

const routesInfo = reactive({
    loading: true,
    pedestrian: {
        duration: {
            text: '...'
        },
        distance: {
            text: '...'
        },
    },
    driving: {
        duration: {
            text: '...'
        },
        distance: {
            text: '...'
        },
    }
})

const selectedTransportType = ref<'pedestrian' | 'driving'>('pedestrian');

watchEffect(async () => {
    routesInfo.loading = true
    if (props.currentUserPosition) {
        const [p, d] = await Promise.all([getRouteData(props.currentUserPosition, props.department.address, 'pedestrian'), getRouteData(props.currentUserPosition, props.department.address, 'driving')])
        routesInfo.pedestrian = p as { duration: { text: string; }; distance: { text: string; }; }
        routesInfo.driving = d as { duration: { text: string; }; distance: { text: string; }; }
    }
    routesInfo.loading = false
})

const daysOfWeek = [
    {
        value: "monday",
        label: "Пн"
    },
    {
        value: "tuesday",
        label: "Вт"
    },
    {
        value: "wednesday",
        label: "Ср"
    },
    {
        value: "thursday",
        label: "Чт"
    },
    {
        value: "friday",
        label: "Пт"
    },
    {
        value: "saturday",
        label: "Сб"
    },
    {
        value: "sunday",
        label: "Вс"
    },
]
const selectedDayOfWeek = ref<{ value: string, label: string } | null>(null);

const hours = [...Array(24).keys()]

const departmentFullness = computed(() => {
  return {0: 'Нет очередей', 1: 'Возможны очереди', 2: 'Высокая загруженность'}[props.department.fullness!]
})

watchEffect(async () => {
  props.department.fullness = (await axiosInstance.post('/fullness_of_department', {department_id: props.department.department_id, date: new Date().getTime()})).data
})
</script>

<style>
.transport-type-card {
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;
    padding: 6px 20px;
    border-radius: 12px;
    width: 100%;
    border: solid 1px var(--text-primary);
    transition: all .3s ease;
    cursor: pointer;
}

.transport-type-card.active {
    color: var(--accent-color);
    border: solid 1px var(--accent-color);
}

.low {
  color: #0E9835
}

.medium {
  color: #FF9900
}

.high {
  color: #CD1919
}

</style>