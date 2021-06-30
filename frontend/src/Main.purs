module Main where

import Prelude
import Z3

import Effect (Effect)
import Effect.Console (log)

sample_request = {url: "http://blum.cs.haverford.edu:8080/checker", body: "{'test':'hello'}"}

main :: Effect Unit
main = do
  sendRequest sample_request