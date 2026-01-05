#!/bin/bash

# Create a Log Analytics Workspace
RESOURCE_GROUP="observability-rg"
WORKSPACE_NAME="log-analytics-workspace"
LOCATION="East US"

az group create --name $RESOURCE_GROUP --location $LOCATION
az monitor log-analytics workspace create \
  --resource-group $RESOURCE_GROUP \
  --workspace-name $WORKSPACE_NAME \
  --location $LOCATION

# Output workspace details
az monitor log-analytics workspace show \
  --resource-group $RESOURCE_GROUP \
  --workspace-name $WORKSPACE_NAME