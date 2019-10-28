import React, { useState } from "react";
import Box from "@material-ui/core/Box"

import PetitionStepper from "./PetitionStepper"
import RecordUploader from "./RecordUploader"
import RecordEdit from "./RecordEdit"
import Analysis from "./Analysis"
import DownloadPetitions from "./DownloadPetitions"
import GettingStarted from "./GettingStarted"

const steps = [
    {
        "label": "Enter applicant information",
        "optional": false,
        "component": <GettingStarted />
    },
    {
        "label": "Upload criminal record files",
        "optional": false,
        "component": <RecordUploader />
    },
    {
        "label": "Edit a record",
        "optional": true,
        "component": <RecordEdit /> 
    },
    {
        "label": "Analyze the record for sealable cases",
        "optional": true,
        "component": <Analysis/>
    },
    {
        "label": "Download petitions",
        "optional": false,
        "component": <DownloadPetitions />
    },
]

function getActiveStep(index) {
    return steps[index]
}

export default function (props) {
    
    const [activeStepIndex, setActiveStepIndex] = useState(0)
   

    return (
        <Box>
            <PetitionStepper steps={steps} activeStepIndex={activeStepIndex} setActiveStepIndex={setActiveStepIndex}>
            </PetitionStepper>
            {   // Insert the setActiveStepIndex into each step, so they can move the user around.
                React.cloneElement(getActiveStep(activeStepIndex).component, 
                {
                    setActiveStepIndex: setActiveStepIndex,
                    activeStepIndex: activeStepIndex
                })
            }
        </Box>
    )
}