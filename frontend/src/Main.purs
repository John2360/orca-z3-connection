module Main where

import Prelude
import Z3

import Effect (Effect)
import Effect.Console (log)

myValue =
          { expressions: "x+y>=2",
            bounds: "x>0",
            types: ""
          } :: MyExpression
sample_request = {url: "http://blum.cs.haverford.edu:8080/checker", body: myValue}


main :: Effect Unit
main = do
  sendRequest sample_request