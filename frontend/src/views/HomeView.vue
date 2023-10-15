<template>
    <div>
        <n-spin :show="isLoadingMap">
            <div style="position: relative; height: 100vh;">
                <n-card class="header" content-style="padding: 12px">
                    <div class="container">
                        <img alt="" src="@/assets/vtb-logo.svg">
                        <n-button @click="rootStore.toggleTheme()">
                            Тема
                        </n-button>
                    </div>
                </n-card>

                <YandexMap
                    :controls="[]"
                    :coordinates="coordinates"
                    :detailed-controls="detailedControls"
                    :events="['boundschange']"
                    :zoom="mapZoom"
                    @boundschange="onBoundsChanged"
                    @created="onMapCreated"
                >
                    <YandexMarker
                        v-if="currentUserPosition"
                        :coordinates="currentUserPosition"
                        :options="{
            iconLayout: 'default#image',
            iconImageHref: userMarkIconBackdrop,
            iconImageSize: [50, 50],
            iconImageOffset: [-25, -25]
        }"
                        marker-id="currentUserPositionBackdrop"
                    />

                    <YandexMarker
                        v-if="currentUserPosition"
                        :coordinates="currentUserPosition"
                        :options="{
            iconLayout: 'default#image',
            iconImageHref: userMarkIcon,
            iconImageSize: [30, 30],
            iconImageOffset: [-15, -15]
        }"
                        marker-id="currentUserPosition"
                    />


                    <YandexClusterer v-if="selectedMarkersMode === 'departs'"
                                     :options="{ preset: 'islands#nightClusterIcons' }">
                        <YandexMarker
                            v-for="department in departmentsInView"
                            :key="`2-marker-${department.department_id}`"
                            :coordinates="[department.latitude, department.longitude]"
                            :marker-id="`2-marker-${department.department_id}`"
                            :options="{
            iconLayout: 'default#image',
            iconImageHref: markGreenIcon,
            iconImageSize: [50, 50],
            iconImageOffset: [-25, -25]
        }"
                        />
                    </YandexClusterer>

                    <YandexClusterer v-if="selectedMarkersMode === 'atms'"
                                     :options="{ preset: 'islands#nightClusterIcons' }">
                        <YandexMarker
                            v-for="atm in atmsInView"
                            :key="`2-marker-${atm.atm_id}`"
                            :coordinates="[atm.latitude, atm.longitude]"
                            :marker-id="`2-marker-${atm.atm_id}`"
                            :options="{
            iconLayout: 'default#image',
            iconImageHref: markGreenIcon,
            iconImageSize: [50, 50],
            iconImageOffset: [-25, -25]
        }"
                        />
                    </YandexClusterer>
                </YandexMap>

                <n-button class="current-location-button" color="white" round style="padding: 8px;"
                          @click="onClickCurrentLocation">
                    <template #icon>
                        <NearMeLocation style="color: black"/>
                    </template>
                </n-button>

                <n-card class="menu-card main-menu p-0" content-style="padding: 0">
                    <transition name="page">
                        <n-card v-if="menuView === 'mainMenu'" class="position-absolute main-menu"
                                content-style="padding: 20px 16px">
                            <MainMenu
                                @to-filters="menuView = 'filters'"
                                :departments="departmentsInView"
                                @update:selected-department-type="(t: 'atms' | 'departs') => selectedMarkersMode = t"
                                @open-depart="onOpenDepart"/>
                        </n-card>
                        <n-card v-else-if="menuView === 'departmentCard' && departmentsInView[0]"
                                class="position-absolute main-menu"
                                content-style="padding: 20px 16px">
                            <DepartmentCard
                                :department="departmentsInView[0]"
                                @back="menuView = 'mainMenu'"
                            />
                        </n-card>
                        <n-card v-else-if="menuView === 'filters'"
                                class="position-absolute main-menu"
                                content-style="padding: 20px 16px">
                            <FiltersMenu
                                @back="menuView = 'mainMenu'"
                                @apply="args => selectedCriteria = args"
                            />
                        </n-card>
                    </transition>
                </n-card>
            </div>
        </n-spin>

        <n-modal :show="isGeolocationRequestShown">
            <n-card style="max-width: 400px">
                <div
                    style="display: flex; justify-content: center; align-items: center; flex-direction: column; text-align: center">
                    <ShareLocation style="width: 100px; color: var(--accent-blue)"/>

                    <h2>Выдайте доступ к геолокации</h2>

                    <p>Он нужен чтобы мы могли найти подходящие отделения и проложить машрут до них</p>

                    <div style="width: 100%; gap: 10px; display: flex; flex-direction: column">
                        <n-button block tertiary type="primary" @click="onClickSetupGeolocation(false)">
                            Продолжить без геолокации
                        </n-button>
                    </div>
                </div>
            </n-card>
        </n-modal>
    </div>
</template>

<script lang="ts" setup>
import {onMounted, Ref, ref} from "vue";
import {loadYmap, YandexClusterer, YandexMap, YandexMarker} from 'vue-yandex-maps'
import ShareLocation from "@components/icons/ShareLocation.vue";
import NearMeLocation from "@components/icons/NearMeLocation.vue";
import {axiosInstance} from "@/api/axiosInstance.ts";
import {Department} from "@data/Department.ts";
import {Atm} from "@data/Atm.ts";
import markGreenIcon from "@/assets/mark-green.svg"
import userMarkIcon from "@/assets/user-mark.svg"
import userMarkIconBackdrop from "@/assets/user-mark-back.png"
import {mapSettings} from "@/main.ts";
import MainMenu from "@components/MainMenu.vue";
import {useRootStore} from "@/store/rootStore.ts";
import DepartmentCard from "@components/DepartmentCard.vue";
import FiltersMenu from "@components/FiltersMenu.vue";

const rootStore = useRootStore();

let yaMap: any = null;
let activeRoute: any = null;
const coordinates = ref([55.7, 37.5]);
const mapZoom = ref(10);
const currentUserPosition = ref<number[] | null>(null) as Ref<number[]>;
const detailedControls = {
    zoomControl: {position: {right: 10, top: 500}}
};

const isGeolocationAvailable = ref(false);
const isGeolocationRequestShown = ref(false);
const isLoadingMap = ref(true);
const checkGeolocationIntervalId = ref(null) as Ref<any>;
const selectedMarkersMode = ref<'departs' | 'atms'>('atms')
const selectedCriteria = ref<
    Array<
        "individual" |
        "privilege" |
        "legalEntity" |
        "prime" |
        "availableForDisabledPeople" |
        "accountsAndCards" |
        "credits" |
        "investments" |
        "servicesForPensioners" |
        "transfers"
    >
>([])

const menuView = ref<'mainMenu' | 'departmentCard' | 'filters'>('mainMenu')
const activeDepart = ref<Department | null>(null) as Ref<Department>;

const onOpenDepart = (depart: Department) => {
    activeDepart.value = depart
    menuView.value = "departmentCard"
}

const geolocationAccessCheck = () => {
    navigator.geolocation.getCurrentPosition((data) => {
        isGeolocationAvailable.value = true;
        isLoadingMap.value = false;
        isGeolocationRequestShown.value = false;
        currentUserPosition.value = [data.coords.latitude, data.coords.longitude];
        coordinates.value = [data.coords.latitude, data.coords.longitude];
        // ymaps.ready(() => {
        //   getRouteData('119620, г. Москва, ул. Богданова, д. 50').then(console.log)
        // })
        // ymaps.ready(() => {
        //   buildRouteOnMap('119620, г. Москва, ул. Богданова, д. 50', 'pedestrian')
        // })
        mapZoom.value = 17;
        clearInterval(checkGeolocationIntervalId.value);
        startWatchingPosition();
    }, () => {
        isLoadingMap.value = true;
        isGeolocationAvailable.value = false;
        isGeolocationRequestShown.value = true;
    })
}

const startWatchingPosition = () => {
    navigator.geolocation.watchPosition(
        (data) => {
            currentUserPosition.value = [data.coords.latitude, data.coords.longitude];
        },
        (error) => {
            if (error.code == error.PERMISSION_DENIED) {
                checkGeolocationIntervalId.value = setInterval(() => {
                    geolocationAccessCheck()
                }, 1000)
            }
        });
}

const onClickSetupGeolocation = (state: boolean) => {
    if (!state) {
        isGeolocationAvailable.value = false
        isLoadingMap.value = false
        isGeolocationRequestShown.value = false
        clearInterval(checkGeolocationIntervalId.value);
    }
}

const onClickCurrentLocation = () => {
    if (!isGeolocationAvailable.value) {
        checkGeolocationIntervalId.value = setInterval(() => {
            geolocationAccessCheck()
        }, 1000)
    } else {
        coordinates.value = currentUserPosition.value.slice()
        mapZoom.value = 18
    }
}

const departmentsInView = ref([] as Department[]);
const atmsInView = ref([] as Atm[]);

const onBoundsChanged = async (e: any) => {
    const res = (await axiosInstance.post('/departments_in_coords', {
        latitude1: e.originalEvent.newBounds[1][0],
        longitude1: e.originalEvent.newBounds[0][1],
        latitude2: e.originalEvent.newBounds[0][0],
        longitude2: e.originalEvent.newBounds[1][1],
    })).data

    departmentsInView.value = res.deps
    atmsInView.value = res.atms
}

onMounted(async () => {
    await loadYmap(mapSettings);
    checkGeolocationIntervalId.value = setInterval(() => {
        geolocationAccessCheck()
    }, 1000)
})

// @ts-ignore
const buildRouteOnMap = (to: string, type: 'pedestrian' | 'driving' = 'driving') => {
    activeRoute = new ymaps.multiRouter.MultiRoute({
        referencePoints: [
            currentUserPosition.value,
            to
        ],
        params: {
            results: 1,
            routingMode: type,
            avoidTrafficJams: true
        }
    }, {
        boundsAutoApply: true
    });

    yaMap?.geoObjects?.add(activeRoute);
}

// @ts-ignore
const clearActiveRoute = () => {
    yaMap?.geoObjects?.remove(activeRoute);
}

// @ts-ignore
const getRouteData = (to: string, type: 'pedestrian' | 'driving' = 'driving') => {
    let multiRoute = new ymaps.multiRouter.MultiRoute({
        referencePoints: [
            currentUserPosition.value,
            to
        ],
        params: {
            results: 1,
            routingMode: type,
            avoidTrafficJams: true
        }
    }, {
        boundsAutoApply: true
    });

    return new Promise((resolve) => {
        multiRoute.model.events.add('requestsuccess', () => {
            const routes = multiRoute.getRoutes();
            for (let i = 0, l = routes.getLength(); i < l; i++) {
                const route = routes.get(i);
                resolve({type: type, duration: route.properties._data.duration, distance: route.properties._data.distance});
            }
        })
    })
}

const onMapCreated = (e: any) => {
    yaMap = e;
}
</script>

<style>
.yandex-container {
    height: 100vh;
    width: 100vw;
    position: absolute;
}

.main-menu {
    border-radius: 16px;
    width: 400px;
    text-align: left;
    height: 100%;
}

.ymaps-2-1-79-gotoymaps__container,
.ymaps-2-1-79-gototech,
.ymaps-2-1-79-gototaxi {
    display: none !important;
}

html[theme='light'] .ymaps-2-1-79-ground-pane {
    filter: grayscale(100%) !important;
    -ms-filter: grayscale(100%) !important;
    -webkit-filter: grayscale(100%) !important;
    -moz-filter: grayscale(100%) !important;
    -o-filter: grayscale(100%) !important;
}

html[theme='dark'] .ymaps-2-1-79-ground-pane {
    filter: invert(100%) grayscale(100%) !important;
    -ms-filter: invert(100%) grayscale(100%) !important;
    -webkit-filter: invert(100%) grayscale(100%) !important;
    -moz-filter: invert(100%) grayscale(100%) !important;
    -o-filter: invert(100%) grayscale(100%) !important;
}

.current-location-button {
    position: absolute;
    right: 10px;
    top: 730px;
}

.menu-card {
    position: absolute;
    top: 80px;
    left: 16px;
    height: calc(100vh - 32px - 80px);
}

.header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 10;
    box-shadow: 0 0 10px 2px rgba(0, 0, 0, .15);
}

.container {
    display: flex;
    justify-content: space-between;
    max-width: 1440px;
    margin: 0 auto;
}

.ymaps-2-1-79-routerRoutes-pane {
    filter: invert(50%) sepia(85%) saturate(3614%) hue-rotate(202deg) brightness(66%) contrast(115%);
}
</style>