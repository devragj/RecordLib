import React from "react";
import Cases from "./Cases";
import Defendant from "./Defendant"

function CRecord(props) {
    const cRecordStyle = {margin: '15px', border: '1px solid black', borderRadius: '25px', padding: '10px', width: '950px'};
    return (
        <div className="cRecord" style={cRecordStyle}>
            <Defendant {...props.defendant}/>
            <Cases cases={props.cases}/>
        </div>
    );
}

export default CRecord;