module Z3 where

import Affjax.RequestHeader
import Data.Map
import Data.Maybe
import Prelude

import Affjax as AX
import Affjax.RequestBody as RequestBody
import Affjax.ResponseFormat as ResponseFormat
import Data.Argonaut.Core (stringify, fromString, Json)
import Data.Either (Either(..))
import Data.HTTP.Method (Method(..))
import Effect (Effect)
import Effect.Aff (Aff, launchAff_)
import Effect.Aff.Compat (EffectFnAff, fromEffectFnAff)
import Effect.Class.Console (log)
import Prim.Boolean (False, True)
import Simple.JSON as JSON

type MyCheck =
  {   expressions :: String
    , bounds :: String
    , types :: String
  }

type MySimplify =
  {   expression :: String
  }

requestCheck :: String->String->String->Effect Unit
requestCheck expressions bounds types = launchAff_ do   
    let myCheck = {expressions : expressions, bounds:bounds,types:types} :: MyCheck
    let url = "http://blum.cs.haverford.edu:8080/checker"
    let headerInfo = [RequestHeader "Content-Type" "application/json"]
    result <- AX.request (AX.defaultRequest { url = url, method = Left POST, responseFormat = ResponseFormat.json, headers = headerInfo, content = (Just(RequestBody.string  (JSON.writeJSON myCheck)))})
    case result of
        Left err -> log $ "POST " <> url <> " response failed to decode: " <> AX.printError err
        Right response -> log $ "POST " <> url <> " response: " <> stringify response.body

requestSimplify :: String -> Effect Unit
requestSimplify expression = launchAff_ do   
    let mySimplify = {expression : expression} :: MySimplify
    let url = "http://blum.cs.haverford.edu:8080/simplify"
    let headerInfo = [RequestHeader "Content-Type" "application/json"]
    result <- AX.request (AX.defaultRequest { url = url, method = Left POST, responseFormat = ResponseFormat.json, headers = headerInfo, content = (Just(RequestBody.string  (JSON.writeJSON mySimplify)))})
    case result of
        Left err -> log $ "POST " <> url <> " response failed to decode: " <> AX.printError err
        Right response -> log $ "POST " <> url <> " response: " <> stringify response.body

statusToBool :: String -> Boolean
statusToBool status
  |status == "sat" = true
  |otherwise = false