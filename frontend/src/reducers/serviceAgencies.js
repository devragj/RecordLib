export default function serviceAgencyReducer(state={result: [], entities: {}}, action) {
    switch (action.type) {
        case 'NEW_SERVICE_AGENCY': 
            return(
                Object.assign(
                    {}, 
                    state, 
                    {
                        result: [...state.result, action.payload.id],
                        entities: Object.assign({}, state.entities, 
                            {
                                [action.payload.id]: {
                                    id: action.payload.id,
                                    name: action.payload.name,
                                }
                            })
                    })
            )

        case 'EDIT_SERVICE_AGENCY':
            return(
                Object.assign(
                    {},
                    state,
                    {
                        entities:  Object.assign({}, state.entities, 
                            {
                                [action.payload.id]: {
                                    id: action.payload.id,
                                    name: action.payload.name,
                                }
                            })

                    }
                )
            )

        case "DELETE_SERVICE_AGENCY":
            const callback = (acc, [k, v]) => Object.assign(acc, {[k]:v})
            const newEntities = Object.entries(state.entities)
                                .filter(([key]) => key !== action.payload.id)
                                .reduce(callback, {})
            
            return(
                Object.assign(
                    {},
                    state,
                    {
                        result: state.result.filter(s => s !== action.payload.id),
                        entities: newEntities,
                    }
                )
            )
        default:
            return(state)
    }
}