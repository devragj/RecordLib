import React from "react";
import PropTypes from 'prop-types';

import AttorneyHolderWrapper from "./AttorneyHolder";
import AddAttorneyWrapper from "./AddAttorney";
import ShowHideList from "./ShowHideList";


function Attorneys(props) {
    const attorneysStyle = { margin: '15px', padding: '10px', width: '900px' };
    const { attorneys } = props;
    const attorneysRendered = attorneys.map(attorneyId => {
            return <AttorneyHolderWrapper key={attorneyId} attorneyId={attorneyId} />
        }
    );

    const addAttorney = <AddAttorneyWrapper key='addAttorney'/>
    attorneysRendered.push(addAttorney);

    return (
        <div className="attorneys" style={attorneysStyle}>
           <ShowHideList hidden={true} title="Attorneys" list={attorneysRendered} />
        </div>
    );
}

Attorneys.propTypes = {
    attorneys: PropTypes.array.isRequired
}


export default Attorneys;