# TODO LIST

## Features
 + Add name to `document_template` and `contract_field` actions;
 + Add to tree view of `res.partner.contract.field` fields: `name`, `description`, `technical_name`, `visible`
 - Change order of `res.partner.document.template` to order by `company_type, document_type, sequence`

## Fixes
 - Change all `parents` to `genitive`
 - Merge `document_type` and `template_type` in `res.partner.document.template`

## Big feature
 - Separate XML actions that generates transient fields for all types of documents
