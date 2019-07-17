#!/bin/bash

set -eu

HOSTNAME="${DOUGHKNOTS_HOSTNAME:-"http://localhost:8000"}"

function inventory() {
  curl -s "${HOSTNAME}/bakery" | jq
}

function bake() {
  kind="$1"
  amount="$2"

  curl -s "${HOSTNAME}/bakery/${kind}" -d "$amount"
}

function order() {
  kind="$1"
  amount="$2"

  curl -s "${HOSTNAME}/shopfront" -d "{\"${kind}\":${amount}}"
}

function operation_names() {
  curl -s "${HOSTNAME}/unknotter/operation_names" | jq
}

function most_recent() {
  operation_name="$1"

  curl -s "${HOSTNAME}/unknotter/traces?operation_name=${operation_name}" | jq '. | sort_by(.duration) | reverse'
}

function fastest() {
  operation_name="$1"

  curl -s "${HOSTNAME}/unknotter/traces?operation_name=${operation_name}&selector=fastest" | jq '. | sort_by(.duration) | reverse'
}

function slowest() {
  operation_name="$1"

  curl -s "${HOSTNAME}/unknotter/traces?operation_name=${operation_name}&selector=slowest" | jq '. | sort_by(.duration) | reverse'
}

function usage() {
  echo -e "doughknots.sh\\n\\tMmm, donuts\\n"
  echo "Usage:"
  echo "  inventory        Check the inventory"
}

function main() {
  cmd="${1:-""}"

  case "$cmd" in
    "-h" | "--help")
      usage
      ;;
    "inventory")
      inventory
      ;;
    "bake")
      kind="$2"
      amount="${3:-"1"}"

      bake "$kind" "$amount"
      ;;
    "order")
      kind="$2"
      amount="${3:-"1"}"

      order "$kind" "$amount"
      ;;
    "operations" | "operation-names" | "operation_names")
      operation_names
      ;;
    "recent" | "most-recent" | "most_recent")
      operation_name="$1"
      most_recent "$operation_name"
      ;;
    "fastest")
      operation_name="$1"
      fastest "$operation_name"
      ;;
    "slowest")
      operation_name="$1"
      slowest "$operation_name"
      ;;
    *)
      usage
      exit 1
      ;;
  esac
}

main "$@"
