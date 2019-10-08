import React, { useState } from "react";
import { connect } from "react-redux"
import Container from "@material-ui/core/Container"
import List from '@material-ui/core/List';
import Button from "@material-ui/core/Button"
import { makeStyles } from '@material-ui/core/styles';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from "@material-ui/core/ListItemText";

import { uploadRecords } from "../actions";
/*
*   Step in the Petition analysis and generation process for uploading files for processing.
*
*   This component is for uploading summary and docket files, sending them to the server, 
*   and receiving the resulting CRecord. 
*/

const useStyles = makeStyles(theme => ({
    root: {
        flexGrow: 1,
        maxWidth: 752,
    },
    demo: {
        backgroundColor: theme.palette.background.paper,
    },
    title: {
        margin: theme.spacing(4, 0, 2),
    },
}))

// Helper component to show a list of the files selected.
function FileList(props) {
    const { selectedFiles } = props;
    if (selectedFiles.length > 0) {
        return(
           <List>
                {selectedFiles.map((f, index) => {
                    return(
                        <ListItem key={index}>
                            <ListItemText primary={f.name}/>
                        </ListItem>
                    )
                })}
           </List> 
        )}
    else {
        return(
            <div> No files selected yet </div>
        )
    }
}


// Component to select files and dispatch api call to upload them.
function RecordUploader(props) {
    const classes=useStyles()

    const [selectedFiles, setSelectedFiles] = useState([]);

    const { uploadRecords } = props;

    const onChangeHandler = event => {
        setSelectedFiles([...event.target.files]);
    }

    const onClickHandler = (e) => {
        e.preventDefault();
        console.log("Uploading " + selectedFiles.length + " files")
        uploadRecords(selectedFiles);
    };


    return(
        <Container className={classes.root}> 
            <h1> Upload files </h1>
            <p> Select the summary and docket files you wish to analyze.</p>
            <FileList selectedFiles={selectedFiles}/>
            <form encType="multipart/form-data" onSubmit={onClickHandler}>
                <input multiple type="file" name="file" onChange={onChangeHandler}/>
                <Button type="submit"> Upload </Button>
            </form>
        </Container>
    )
}


function mapStateToProps(state) {
    return {};
};

function mapDispatchToProps(dispatch) {
    return { uploadRecords: files => dispatch(uploadRecords(files)) };
};



export default connect(mapStateToProps, mapDispatchToProps)(RecordUploader)