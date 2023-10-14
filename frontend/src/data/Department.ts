export type Department = {
    department_id: number,
    address: string,
    salePointName: string,
    openHours: [
        {
            days: string,
            hours: null
        }
    ],
    rko: string,
    openHoursIndividual: {
      days: string,
      hours: string
    }[],
    officeType: string,
    salePointFormat: string,
    suoAvailability: string,
    hasRamp: string,
    latitude: number,
    longitude: number,
    metroStation: string,
    distance: number,
    kep: boolean,
    myBranch: boolean
}