#!/bin/bash

(cd frontend && yarn build && cp -a build/. ../backend/static/)
(cd backend && gcloud app deploy)
