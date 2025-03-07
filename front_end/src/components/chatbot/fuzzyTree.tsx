import React, { useEffect, useState } from 'react';
import Tree from 'react-d3-tree';

// This is a simplified example of an org chart with a depth of 2.
// Note how deeper levels are defined recursively via the `children` property.
const orgChart2 = {
  "name": 'CEO',
  children: [
    {
      name: 'Manager',
      attributes: {
        "value": '15.54',
        "alpha-cut": '12'
      },
      children: [
        {
          name: 'Foreman',
          attributes: {
            department: 'Fabrication',
          },
          children: [
            {
              name: 'Worker',
            },
          ],
        },
        {
          name: 'Foreman',
          attributes: {
            department: 'Assembly',
          },
          children: [
            {
              name: 'Worker',
            },
          ],
        },
      ],
    },
    {
      name: 'Manager',
      attributes: {
        "value": '15.54',
        "alpha-cut": '12'
      },}
  ],
};

export default function FuzzyTree() {

  const [orgChart, setOrgChart] = useState<any>({name: 'CEO'});

  useEffect(() => {
    const transformedData = transformTreeToOrgChart(JSON.parse(localStorage.getItem("tree") || '[]'));
    console.log(transformedData);
    setOrgChart(transformedData);
  }, []);
  return (
    <div style={{ width: '100%', height: '100vh', display:'flex', justifyContent:'center',alignItems:'center' }}>
    <Tree orientation='vertical' data={orgChart}   pathFunc={'straight'} />
  </div>
  )
}

const transformTreeToOrgChart = (node: any): any => {
  if (!node || typeof node !== "object") return {}; // Ensure node is valid

  return {
    name: node.name,
    attributes: node.value !== undefined && node.alpha_cut !== undefined
      ? { value: node.value.toFixed(2), "alpha-cut": node.alpha_cut.toFixed(2) }
      : undefined, // Only include attributes if they exist
    children: node.children && node.children.length > 0
      ? node.children.map(transformTreeToOrgChart)
      : undefined, // Avoid empty children arrays
  };
};
