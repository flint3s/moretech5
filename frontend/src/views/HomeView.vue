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


          <YandexClusterer v-if="selectedMarkersMode === 'departs' && !isFiltersSelected" :options="{ preset: 'islands#nightClusterIcons' }">
            <YandexMarker
                v-for="department in departmentsInView"
                :key="`2-marker-${department.department_id}`"
                :coordinates="[department.latitude, department.longitude]"
                :events="['click']"
                :marker-id="`2-marker-${department.department_id}`"
                :options="{
            iconLayout: 'default#image',
            iconImageHref: department.fullness === 0 ? markGreenIcon : department.fullness === 1 ? markYellowIcon : department.fullness === 2 ? markRedIcon : markBlueIcon,
            iconImageSize: [50, 50],
            iconImageOffset: [-25, -25]
        }"
                @click="onOpenDepart(department)"
            />
          </YandexClusterer>
          <YandexClusterer v-else-if="selectedMarkersMode === 'departs' && isFiltersSelected" :options="{ preset: 'islands#nightClusterIcons' }">
            <YandexMarker
                v-for="department in searchDepartments"
                :key="`2-marker-${department.department_id}`"
                :coordinates="[department.latitude, department.longitude]"
                :events="['click']"
                :marker-id="`2-marker-${department.department_id}`"
                :options="{
            iconLayout: 'default#image',
            iconImageHref: department.fullness === 0 ? markGreenIcon : department.fullness === 1 ? markYellowIcon : department.fullness === 2 ? markRedIcon : markBlueIcon,
            iconImageSize: [50, 50],
            iconImageOffset: [-25, -25]
        }"
                @click="onOpenDepart(department)"
            />
          </YandexClusterer>

          <YandexClusterer v-if="selectedMarkersMode === 'atms'" :options="{ preset: 'islands#nightClusterIcons' }">
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

        <n-card v-if="activeRouterInfo.isActive"
                class="route-status"
                content-style="display: flex; gap: 12px; align-items: center; justify-content: center">
          <n-button text type="primary" @click="clearActiveRoute">
            <template #icon>
              <CloseIcon/>
            </template>

            Отменить
          </n-button>

          <span v-if="activeRouterInfo.isActive" class="fw-bold" style="font-size: 16px">
            {{ activeRouterInfo.duration.text }}. · {{ activeRouterInfo.distance.text }}
          </span>
        </n-card>

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
                  :atms="atmsInView"
                  :departments="departmentsInView"
                  :filters="selectedFilters"
                  :mode="searchDepartments.length > 0 ? 'search-departs' : selectedMarkersMode"
                  :search-departments="searchDepartments"
                  @update:date="t => selectedTime = t"
                  @to-filters="menuView = 'filters'"
                  @update:selected-department-type="(t: 'atms' | 'departs') => selectedMarkersMode = t"
                  @open-depart="onOpenDepart"
                  @zoom-atm="onZoomAtm"
              />
            </n-card>
            <n-card v-else-if="menuView === 'departmentCard' && activeDepart"
                    class="position-absolute main-menu"
                    content-style="padding: 20px 16px">
              <DepartmentCard
                  :current-user-position="currentUserPosition"
                  :department="activeDepart"
                  :is-geolocation-available="isGeolocationAvailable"
                  @back="menuView = 'mainMenu'"
                  @build-route="buildRouteOnMap(activeDepart.address)"
              />
            </n-card>
            <n-card v-else-if="menuView === 'filters'"
                    class="position-absolute main-menu"
                    content-style="padding: 20px 16px">
              <keep-alive>
                <FiltersMenu
                    :filters="selectedFilters"
                    @back="menuView = 'mainMenu'"
                    @update:filters="onFiltersApply"
                />
              </keep-alive>
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
import {onMounted, Ref, ref, watchEffect} from "vue";
import {loadYmap, YandexClusterer, YandexMap, YandexMarker} from 'vue-yandex-maps'
import ShareLocation from "@components/icons/ShareLocation.vue";
import NearMeLocation from "@components/icons/NearMeLocation.vue";
import {axiosInstance} from "@/api/axiosInstance.ts";
import {Department} from "@data/Department.ts";
import {Atm} from "@data/Atm.ts";
import markGreenIcon from "@/assets/mark-green.svg"
import markYellowIcon from "@/assets/mark-yellow.svg"
import markBlueIcon from "@/assets/mark-blue.svg"
import markRedIcon from "@/assets/mark-red.svg"
import userMarkIcon from "@/assets/user-mark.svg"
import userMarkIconBackdrop from "@/assets/user-mark-back.png"
import {mapSettings} from "@/main.ts";
import MainMenu from "@components/MainMenu.vue";
import {useRootStore} from "@/store/rootStore.ts";
import DepartmentCard from "@components/DepartmentCard.vue";
import FiltersMenu from "@components/FiltersMenu.vue";
import CloseIcon from "@/views/CloseIcon.vue";
import {getRouteData} from "@data/computeRoute.ts";

const rootStore = useRootStore();

let yaMap: any = null;
let activeRoute: any = null;
const activeRouterInfo = reactive({
  isActive: false,
  to: '',
  type: 'pedestrian',
  duration: {
    text: '...'
  },
  distance: {
    text: '...'
  }
})
const coordinates = ref([55.7, 37.5]);
const mapZoom = ref(10);
const currentUserPosition = ref<number[] | null>(null) as Ref<number[]>;
const detailedControls = {
  zoomControl: {position: {right: 10, top: window.innerWidth >= 576 ? 500 : 100}}
};

const searchDepartments = ref([] as Department[]);
const selectedFilters = reactive({
  coords: {
    latitude: 0,
    longitude: 0
  },
  entity: "",
  feature: "",
  full_mobility: false,
  services: []
})

const isFiltersSelected = computed(() => {
  return !!selectedFilters.entity || !!selectedFilters.feature || !!selectedFilters.services.length || selectedFilters.full_mobility
})

watchEffect(async () => {
  if (!isFiltersSelected.value) {
    searchDepartments.value = []
  } else {
    const data = (await axiosInstance.post('/nearest_departments_by_coords', selectedFilters)).data as Department[]
    data.reverse()
    if (currentUserPosition.value) {
      (await Promise.all(data.map(d => getRouteData(currentUserPosition.value, d.address, 'pedestrian')))).map((r: any, i) => {
        data[i].routeData = {duration: '', distance: ''}
        data[i].routeData!.duration = r.duration.text
        data[i].routeData!.distance = r.distance.text
      })
    }

    (await Promise.all(data.map(d => axiosInstance.post('/fullness_of_department', {date: selectedTime.value, department_id: d.department_id})))).map(r => r.data).forEach((f, i) => data[i].fullness = f)

    searchDepartments.value = data
    coordinates.value = [searchDepartments.value[0].latitude, searchDepartments.value[0].longitude]
    mapZoom.value = 17
  }
})


const onFiltersApply = (args: any) => {
  menuView.value = 'mainMenu';
  selectedFilters.services = args.services;
  selectedFilters.full_mobility = args.full_mobility;
  selectedFilters.feature = args.feature;
  selectedFilters.entity = args.entity;
  selectedFilters.coords.latitude = currentUserPosition.value[0]
  selectedFilters.coords.longitude = currentUserPosition.value[1]
}

const isGeolocationAvailable = ref(false);
const isGeolocationRequestShown = ref(false);
const isLoadingMap = ref(true);
const checkGeolocationIntervalId = ref(null) as Ref<any>;
const selectedMarkersMode = ref<'departs' | 'atms'>('atms')
const selectedTime = ref(new Date().getTime());

const menuView = ref<'mainMenu' | 'departmentCard' | 'filters'>('mainMenu')
const activeDepart = ref<Department | null>(null) as Ref<Department>;

const onOpenDepart = (depart: Department) => {
  activeDepart.value = depart
  menuView.value = "departmentCard"
  coordinates.value = [depart.latitude, depart.longitude]
  mapZoom.value = 18
}

const onZoomAtm = (atm: Atm) => {
  coordinates.value = [atm.latitude, atm.longitude]
  mapZoom.value = 18
}

const geolocationAccessCheck = () => {
  navigator.geolocation.getCurrentPosition((data) => {
    isGeolocationAvailable.value = true;
    isLoadingMap.value = false;
    isGeolocationRequestShown.value = false;
    currentUserPosition.value = [data.coords.latitude, data.coords.longitude];
    coordinates.value = [data.coords.latitude, data.coords.longitude];
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

        if (activeRouterInfo.isActive) {
          console.log('route rebuild')
          clearActiveRoute()
          buildRouteOnMap(activeRouterInfo.to, activeRouterInfo.type as "pedestrian" | "driving")
        }
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
    date: selectedTime.value
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

const buildRouteOnMap = async (to: string, type: 'pedestrian' | 'driving' = 'driving') => {
  clearActiveRoute()

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

  const data = (await getRouteData(currentUserPosition.value, to)) as any;
  activeRouterInfo.isActive = true;
  activeRouterInfo.type = type;
  activeRouterInfo.to = to;
  [activeRouterInfo.duration, activeRouterInfo.distance] = [data.duration, data.distance];
}

const clearActiveRoute = () => {
  yaMap?.geoObjects?.remove(activeRoute);
  activeRouterInfo.isActive = false
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

.route-status {
  position: absolute;
  top: 80px;
  left: 40%;
  max-width: 300px;
  border-radius: 16px;
}

@media screen and (max-width: 576px) {
  .menu-card {
    left: calc(5% / 2);
    width: 95%;
    height: 400px;
    overflow-y: auto;
    overflow-x: hidden;
    top: calc(100% - 416px);
  }

  .current-location-button {
    top: 320px;
    right: 8px;
  }

  .route-status {
    top: 80px;
    left: 10%;
    width: 90%;
  }
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