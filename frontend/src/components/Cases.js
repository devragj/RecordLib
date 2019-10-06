import React from "react";
import PropTypes from 'prop-types';

import CaseHolderWrapper from "./CaseHolder";
import ShowHideList from "./ShowHideList";


function Cases(props) {
    const casesStyle = {margin: '15px', padding: '10px', width: '900px'};
    const { cases } = props;
    const casesRendered = cases.map(caseId => {
            return <CaseHolderWrapper key={caseId} caseId={caseId} />
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