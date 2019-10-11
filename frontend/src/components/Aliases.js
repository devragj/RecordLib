import React from "react";
import PropTypes from 'prop-types';

import AliasHolderWrapper from "./AliasHolder";
import AddAliasWrapper from "./AddAlias";
import ShowHideList from "./ShowHideList";


function Aliases(props) {
    const aliasesStyle = {gridColumn: "1 / 4"};
    const { aliases, editing } = props;
    const aliasesRendered = aliases.map(aliasId => {
            return <AliasHolderWrapper key={aliasId} aliasId={aliasId} editing={editing}/>
        }
    );

    if (editing) {
        const addAliasKey = 'addAlias';
        const addAlias = <AddAliasWrapper key={addAliasKey}/>
        aliasesRendered.push(addAlias);
    };

    return (
        <div className="aliases" style={aliasesStyle}>
        {aliasesRendered.length > 0 &&
           <ShowHideList hidden={!editing} title="Aliases" list={aliasesRendered} />
        }
        </div>
    );
}

Aliases.propTypes = {
    /**
        The list of alias ids.
    */
    aliases: PropTypes.array.isRequired,
    /**
        This component wil be used either in the Case component,
        in which case editing is false, or in the EditCase
        component, in which case editing is true.
    */
    editing: PropTypes.bool
}

export default Aliases;