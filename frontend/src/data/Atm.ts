export type Atm = {
  atm_id: number,
  address: string,
  latitude: number,
  longitude: number,
  allDay: boolean,
  wheelchair: {
    serviceCapability: "UNKNOWN" | "UNAVAILABLE" | "AVAILABLE",
    serviceActivity: "UNKNOWN" | "UNAVAILABLE" | "AVAILABLE"
  },
  blind: {
    serviceCapability: "UNKNOWN" | "UNAVAILABLE" | "AVAILABLE",
    serviceActivity: "UNKNOWN" | "UNAVAILABLE" | "AVAILABLE"
  },
  nfcForBankCards: {
    serviceCapability: "UNKNOWN" | "UNAVAILABLE" | "AVAILABLE",
    serviceActivity: "UNKNOWN" | "UNAVAILABLE" | "AVAILABLE"
  },
  qrRead: {
    serviceCapability: "UNKNOWN" | "UNAVAILABLE" | "AVAILABLE",
    serviceActivity: "UNKNOWN" | "UNAVAILABLE" | "AVAILABLE"
  },
  supportsUsd: {
    serviceCapability: "UNKNOWN" | "UNAVAILABLE" | "AVAILABLE",
    serviceActivity: "UNKNOWN" | "UNAVAILABLE" | "AVAILABLE"
  },
  supportsChargeRub: {
    serviceCapability: "UNKNOWN" | "UNAVAILABLE" | "AVAILABLE",
    serviceActivity: "UNKNOWN" | "UNAVAILABLE" | "AVAILABLE"
  },
  supportsEur: {
    serviceCapability: "UNKNOWN" | "UNAVAILABLE" | "AVAILABLE",
    serviceActivity: "UNKNOWN" | "UNAVAILABLE" | "AVAILABLE"
  },
  supportsRub: {
    serviceCapability: "UNKNOWN" | "UNAVAILABLE" | "AVAILABLE",
    serviceActivity: "UNKNOWN" | "UNAVAILABLE" | "AVAILABLE"
  }
}