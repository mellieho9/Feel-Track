import type { ComponentType } from "react"
import { createStore } from "https://framer.com/m/framer/store.js@^1.0.0"
import { randomColor } from "https://framer.com/m/framer/utils.js@^0.9.0"

// Learn more: https://www.framer.com/docs/guides/overrides/

const useStore = createStore({
    background: "#0099FF",
})

export function withRotate(Component): ComponentType {
    return (props) => {
        return (
            <Component
                {...props}
                animate={{ rotate: 90 }}
                transition={{ duration: 2 }}
            />
        )
    }
}

export function withHover(Component): ComponentType {
    return (props) => {
        return <Component {...props} whileHover={{ scale: 1.05 }} />
    }
}

export function withRandomColor(Component): ComponentType {
    return (props) => {
        const [store, setStore] = useStore()

        return (
            <Component
                {...props}
                animate={{
                    background: store.background,
                }}
                onClick={() => {
                    setStore({ background: randomColor() })
                }}
            />
        )
    }
}
