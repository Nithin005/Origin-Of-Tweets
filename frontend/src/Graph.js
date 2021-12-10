/* eslint-disable react-hooks/exhaustive-deps */
import React, { useState, useCallback, useEffect } from 'react';
import ReactFlow, {
  ReactFlowProvider,
  addEdge,
  removeElements,
  isNode,
} from 'react-flow-renderer';
import dagre from 'dagre';

import initialElements from './initial-elements';

import './layouting.css';
import { getNewResults } from './new';
// import 'react-flow-renderer/dist/layouting.css';
import ReactJson from 'react-json-view'
import config from './config';

const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));

// In order to keep this example simple the node width and height are hardcoded.
// In a real world app you would use the correct width and height values of
// const nodes = useStoreState(state => state.nodes) and then node.__rf.width, node.__rf.height

const nodeWidth = 172;
const nodeHeight = 36;

function convertResultsToGraph(results, engine){
    const _results = {};
    const position = { x: 0, y: 0 };
    const elements = [];
    elements.push({
        id: engine,
        data: {label: engine},
        position
    })
    for(const result of results){
        const id = result['timestamp']
        const el = {
            id: id,
            data: {label: result['author']},
            position,
        }
        elements.push(el);

        const link = {
            id: 'e'+id,
            source: id,
            target: engine,
            type: "edgeType",
            animated: true
        }
        elements.push(link)
        _results[result['timestamp']] = result
    }
    console.log(elements)
    return [elements, _results]
}

const getLayoutedElements = (elements, direction = 'TB') => {
  const isHorizontal = direction === 'LR';
  dagreGraph.setGraph({ rankdir: direction });

  elements.forEach((el) => {
    if (isNode(el)) {
      dagreGraph.setNode(el.id, { width: nodeWidth, height: nodeHeight });
    } else {
      dagreGraph.setEdge(el.source, el.target);
    }
  });

  dagre.layout(dagreGraph);

  return elements.map((el) => {
    if (isNode(el)) {
      const nodeWithPosition = dagreGraph.node(el.id);
      el.targetPosition = isHorizontal ? 'left' : 'top';
      el.sourcePosition = isHorizontal ? 'right' : 'bottom';
      console.log(el)

      // unfortunately we need this little hack to pass a slightly different position
      // to notify react flow about the change. Moreover we are shifting the dagre node position
      // (anchor=center center) to the top left so it matches the react flow node anchor point (top left).
      el.position = {
        x: nodeWithPosition.x - nodeWidth / 2 + Math.random() / 1000,
        y: nodeWithPosition.y - nodeHeight / 2,
      };
    }

    return el;
  });
};

const layoutedElements = getLayoutedElements(initialElements);

const LayoutFlow = () => {
  const [elements, setElements] = useState(layoutedElements);
  const [resultsDB, setResultsDB] = useState({});
  const [currentResult, setCurrentResult] = useState({text: 'data will show here'});
  const onConnect = (params) =>
    setElements((els) =>
      addEdge({ ...params, type: 'smoothstep', animated: true }, els)
    );
  const onElementsRemove = (elementsToRemove) =>
    setElements((els) => removeElements(elementsToRemove, els));

  const onLayout = useCallback(
    (direction) => {
      const layoutedElements = getLayoutedElements(elements, direction);
      setElements(layoutedElements);
    },
    [elements]
  );

  useEffect(async() => {
      const results = await getNewResults({stream: 1});
      console.log(results);
      const [elements, resultsDB] = convertResultsToGraph(results, config.engine);
      const layoutedElements = getLayoutedElements(elements, 'TB');
      setElements(layoutedElements);
      setResultsDB(resultsDB);
  }, []);

  return (
      <div className='graph-row'>
    <div className="layoutflow graph-left" style={{ height: '500'}}>
      <ReactFlowProvider>
        <ReactFlow
          elements={elements}
          onConnect={onConnect}
          onElementsRemove={onElementsRemove}
          connectionLineType="smoothstep"
          onClick={(e)=>{console.log(resultsDB[e.target.dataset['id']]); setCurrentResult(resultsDB[e.target.dataset['id']])}}
        />
        <div className="controls">
          <button onClick={() => onLayout('TB')}>vertical layout</button>
          <button onClick={() => onLayout('LR')}>horizontal layout</button>
          <button onClick={() => onLayout('LR')}>init Graph</button>
        </div>
      </ReactFlowProvider>
    </div>
    <div className="layout graph-right" style={{ height: '100%'}}><ReactJson src={currentResult} /></div>
    </div>
  );
};

export default LayoutFlow;