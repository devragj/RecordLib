import React from "react";
import PropTypes from 'prop-types';

import Case from "./Case";
import ShowHideList from "./ShowHideList";


function Cases(props) {
    const casesStyle = {margin: '15px', padding: '10px', width: '900px'};
    const cases = props.cases
    const casesRendered = cases.map((caseObject, index) => {

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

Cases.propTypes = {
    cases: PropTypes.array.isRequired
}


export default Cases;