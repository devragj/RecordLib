import React from "react";
import Case from "./Case";
import ShowHideList from "./ShowHideList";


function Cases(props) {
    const casesStyle = {margin: '15px', padding: '10px', width: '900px'};
    const casesRendered = props.cases.map((caseObject, index) => {
            const id = caseObject.docket_number;
            return <Case {...caseObject} key={id} id={id}/>
        }
    );

    return (
        <div className="cases" style={casesStyle}>
           <ShowHideList hidden={false} title="Cases" list={casesRendered} />
        </div>
    );
}

export default Cases;