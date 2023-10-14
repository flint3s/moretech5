<template>
  <div>
    <n-spin :show="isLoadingMap">
      <div style="position: relative; height: 100vh;">
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


          <YandexClusterer v-if="selectedMarkersMode === 'departs'" :options="{ preset: 'islands#nightClusterIcons' }">
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

        <n-button class="current-location-button" color="white" round style="padding: 8px;"
                  @click="onClickCurrentLocation">
          <template #icon>
            <NearMeLocation style="color: black"/>
          </template>
        </n-button>
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

.ymaps-2-1-79-gotoymaps__container,
.ymaps-2-1-79-gototech,
.ymaps-2-1-79-gototaxi {
  display: none !important;
}

.ymaps-2-1-78-ground-pane {
  filter: invert(100%) !important;
  -ms-filter: invert(100%) !important;
  -webkit-filter: invert(100%) !important;
  -moz-filter: invert(100%) !important;
  -o-filter: invert(100%) !important;
}

.current-location-button {
  position: absolute;
  right: 10px;
  top: 730px;
}
</style>