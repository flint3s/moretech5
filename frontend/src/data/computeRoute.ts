export const getRouteData = (from: string | number[], to: string | number[], type: 'pedestrian' | 'driving' = 'driving') => {
  let multiRoute = new (window as any).ymaps.multiRouter.MultiRoute({
    referencePoints: [
      from,
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