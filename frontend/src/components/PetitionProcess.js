import React, { useState } from "react";
import Box from "@material-ui/core/Box"
import PetitionStepper from "./PetitionStepper"

import RecordUploader from "./RecordUploader"

const steps = [
    {
        "label": "Upload criminal record files",
        "optional": false,
        "component": <RecordUploader />
    },
    {
        "label": "Edit a record",
        "optional": true,
        "component": <h1> The second step </h1>
    },
    {
        "label": "Analyze the record for sealable cases",
        "optional": true,
        "component": <h1> The third step </h1>
    },
    {
        "label": "Download petitions",
        "optional": false,
        "component": <h1> The last step </h1>
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
            {getActiveStep(activeStepIndex).component}
        </Box>
    )
}