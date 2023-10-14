import {defineStore} from "pinia";

export const useRootStore = defineStore("root", {
    state() {
        return {
            theme: 'light' as 'light' | 'dark',
        }
    },
    actions: {
        initTheme() {
            this.setTheme(localStorage.getItem('app-theme') as 'light' | 'dark' || 'light')
        },
        setTheme(theme: 'light' | 'dark') {
            this.theme = theme
            document.documentElement.setAttribute('theme', theme)
            localStorage.setItem('app-theme', theme)
        },
        toggleTheme() {
            if (this.theme === 'light') {
                this.setTheme('dark')
            } else {
                this.setTheme('light')
            }
        }
    }
})