import {
  IExecuteFunctions,
  INodeExecutionData,
  INodeType,
  INodeTypeDescription,
  NodeOperationError,
} from 'n8n-workflow';

export class WorkspaceConnector implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'Workspace Connector',
    name: 'workspaceConnector',
    icon: 'fa:network-wired',
    group: ['transform'],
    version: 1,
    description: 'Trigger actions and exchange data with the local OMEGA workspace',
    defaults: {
      name: 'Workspace Connector',
    },
    inputs: ['main'],
    outputs: ['main'],
    properties: [
      {
        displayName: 'Resource',
        name: 'resource',
        type: 'options',
        options: [
          {
            name: 'Pipeline',
            value: 'pipeline',
          },
          {
            name: 'Outreach',
            value: 'outreach',
          },
          {
            name: 'Health',
            value: 'health',
          },
        ],
        default: 'pipeline',
        noDataExpression: true,
        required: true,
      },
      {
        displayName: 'Operation',
        name: 'operation',
        type: 'options',
        displayOptions: {
          show: {
            resource: ['pipeline'],
          },
        },
        options: [
          {
            name: 'Trigger Event',
            value: 'triggerEvent',
            action: 'Trigger an event in the local pipeline',
          },
          {
            name: 'Fetch State',
            value: 'fetchState',
            action: 'Fetch current status of the pipeline',
          },
        ],
        default: 'triggerEvent',
        noDataExpression: true,
      },
      {
        displayName: 'Event Name',
        name: 'eventName',
        type: 'string',
        displayOptions: {
          show: {
            resource: ['pipeline'],
            operation: ['triggerEvent'],
          },
        },
        default: 'DATA_INGESTED',
        description: 'The name of the event to broadcast',
      },
    ],
  };

  async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    const items = this.getInputData();
    const returnData: INodeExecutionData[] = [];

    const resource = this.getNodeParameter('resource', 0) as string;

    for (let i = 0; i < items.length; i++) {
      try {
        if (resource === 'pipeline') {
          const operation = this.getNodeParameter('operation', i) as string;
          if (operation === 'triggerEvent') {
            const eventName = this.getNodeParameter('eventName', i) as string;
            returnData.push({
              json: {
                success: true,
                event: eventName,
                timestamp: new Date().toISOString(),
                inputItem: items[i].json,
              },
            });
          } else {
            returnData.push({
              json: {
                success: true,
                status: 'IDLE',
                version: '1.0.0',
              },
            });
          }
        } else {
          returnData.push({
            json: {
              success: true,
              resource,
              timestamp: new Date().toISOString(),
            },
          });
        }
      } catch (error) {
        if (this.continueOnFail()) {
          returnData.push({ json: { error: (error as Error).message } });
          continue;
        }
        throw new NodeOperationError(this.getNode(), error as Error, { itemIndex: i });
      }
    }

    return [returnData];
  }
}
