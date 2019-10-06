import React, {useState} from "react"
import { makeStyles } from "@material-ui/core/styles"
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';


import { connect } from 'react-redux';
import { fetchCRecord } from "../actions";
import CRecordWrapper from "./CRecord"





const useStyles = makeStyles(theme => ({
  root: {
    width: '100%',
  },
  button: {
    marginRight: theme.spacing(1),
  },
  instructions: {
    marginTop: theme.spacing(1),
    marginBottom: theme.spacing(1),
  },
}));


function getSteps() {
    return (["Upload criminal record files", "Edit a record", "Analyze the record for sealable cases", "Download Petitions"])
}




function PetitionStepper(props) {

    const classes = useStyles()
    const [activeStep, setActiveStep] = useState(0)
    const [skipped, setSkipped] = React.useState(new Set());
    const steps = getSteps();

    const [selectedFile, setSelectedFile] = useState(null);

    const { cRecordPresent, fetchCRecord } = props;
    const onChangeHandler = event => {
        setSelectedFile(event.target.files[0]);
    }

    const onClickHandler = () => {
        fetchCRecord(selectedFile);
    };

   return (
        <div className={classes.root}>
            <Stepper activeStep={activeStep}> 
                {steps.map((label, index) => {
                    return (
                        <Step key={label}> 
                            <StepLabel>{label}</StepLabel>
                        </Step>
                    )
                })}
            </Stepper>

            <h2> Upload Files </h2>
            <div >
                <input type="file" name="file" onChange={onChangeHandler}/>
                <button type="button" onClick={onClickHandler} style={{
                    marginLeft: '20px'
                }}>Upload</button>
            </div>
            {cRecordPresent && <CRecordWrapper />}
        </div>
    )
}

function mapStateToProps(state) {
    return { cRecordPresent: state.entities? true: false };
};

function mapDispatchToProps(dispatch) {
    return { fetchCRecord: file => dispatch(fetchCRecord(file)) };
};

export default connect(mapStateToProps, mapDispatchToProps)(PetitionStepper);
