import React, { useState } from "react"
import { connect } from "react-redux"
import FormControl from "@material-ui/core/FormControl"
import InputLabel from "@material-ui/core/InputLabel"
import TextField from "@material-ui/core/TextField"
import PropTypes from 'prop-types';
import List from "@material-ui/core/List"
import ListItem from "@material-ui/core/ListItem"
import IconButton from "@material-ui/core/IconButton"
import DeleteIcon from '@material-ui/icons/Delete';

import { updateServiceAgency, createNewServiceAgency, deleteServiceAgency } from "../actions"


/**
 * List for displaying the service agencies that should receive a set of petitions. 
 * @param {} props 
 */
function ServiceAgencyList(props) {
    const { serviceAgencies, updateServiceAgency, createNewServiceAgency, deleteServiceAgency } = props
   
    const [needAnother, setNeedAnother] = useState(true)
    const [newServiceAgencyName, setNewServiceAgencyName] = useState('');


    const handleSAEdit = (e) => {
        updateServiceAgency(e.target.id, e.target.value)
    }

    const handleNewServiceAgencyChange = (e) => {
        setNewServiceAgencyName(e.target.value);
    }

    const handleNewServiceAgencyComplete = (e) => {
        if (e.target.value.length > 0) {
            // Only create the new service agency if some text was entered into the field.
            createNewServiceAgency({
                id: "serviceAgency" + (serviceAgencies.result.length + 1).toString(),
                name: newServiceAgencyName
            })
            setNewServiceAgencyName('');
        }
    }

    const createHandleDeleteSA = (id) => {
        return ((e) => {
            deleteServiceAgency(id)
        })
    }

    const handleKeyDown = event => {
        if (event.keyCode === 13) {
            event.preventDefault();
            event.stopPropagation();
            handleNewServiceAgencyComplete(event);
        }
    }


    return(
        <div>
            <h5> Service Agencies to list in Petitions.</h5>
            <List>
                {serviceAgencies.result.map(idx => {
                    return(
                        <ListItem key={serviceAgencies.entities[idx].id}>
                            <TextField 
                                id={serviceAgencies.entities[idx].id} 
                                label="Service Agency" 
                                value={serviceAgencies.entities[idx].name}
                                onChange={handleSAEdit}
                                margin="normal"
                                variant="filled"/>
                            <IconButton aria-label="delete" onClick={createHandleDeleteSA(serviceAgencies.entities[idx].id)}>
                                <DeleteIcon />

                            </IconButton>
                        </ListItem>
                    )
                })}
                {
                    needAnother ? 
                    <ListItem key={"newServiceAgency"}>
                        <TextField
                            label="Service Agency"
                            value={newServiceAgencyName}
                            onChange={handleNewServiceAgencyChange}
                            onBlur={handleNewServiceAgencyComplete}
                            onKeyDown={handleKeyDown}
                            margin="normal"
                            variant="filled" /> 
                    </ListItem> :
                        ""
                    }
            </List>
        </div>
    ) 
}


function mapStateToProps(state) {
    return {
        serviceAgencies: state.serviceAgencies
    }
}

function mapDispatchToProps(dispatch) {
    return {
        updateServiceAgency: (id, value) => dispatch(updateServiceAgency(id, value)),
        createNewServiceAgency: (serviceAgency) => dispatch(createNewServiceAgency(serviceAgency)),
        deleteServiceAgency: (id) => dispatch(deleteServiceAgency(id))
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(ServiceAgencyList)