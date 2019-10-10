import React from "react"
import { makeStyles } from "@material-ui/core/styles"
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepButton from '@material-ui/core/StepButton';
import { Typography } from "@material-ui/core";

/*
* A stepper navigation bar that is used to click among steps of a process.
*
*/



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

function PetitionStepper(props) {

    const { steps, activeStepIndex, setActiveStepIndex} = props
    const classes = useStyles()

    return (
        <div className={classes.root}>
            <Stepper nonLinear activeStep={activeStepIndex}> 
                {steps.map((step, index) => {
                    const label = step.label
                    const buttonProps = {};
                    if (step.optional) {
                        buttonProps.optional = <Typography variant="caption"> Optional </Typography>
                    }
                    buttonProps.onClick = () => {setActiveStepIndex(index)}
                    return (
                        <Step key={label}> 
                            <StepButton {...buttonProps}>{label}</StepButton>
                        </Step>
                    )
                })}
            </Stepper>
        </div>
    )
}

export default PetitionStepper;
