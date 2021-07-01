module Z3 where

import Prelude
import Data.Maybe
import Data.Map
import Data.Either (Either(..))
import Affjax as AX
import Affjax.ResponseFormat as ResponseFormat
import Data.Argonaut.Core (stringify, fromString, Json)
import Effect.Class.Console (log)

import Data.HTTP.Method (Method(..))
import Affjax.RequestHeader
import Effect (Effect)
import Effect.Aff (Aff, launchAff_)
import Effect.Aff.Compat (EffectFnAff, fromEffectFnAff)

import Affjax.RequestBody as RequestBody
import Simple.JSON as JSON

type MyCheck =
  {   expressions :: String
    , bounds :: String
    , types :: String
  }

type MySimplify =
  {   expression :: String
  }

type API_Requests = {
    url :: String,
    body :: MyCheck
}

type API_Requests2 = {
    url :: String,
    body :: MySimplify
}

--sample = {url:"http://blum.cs.haverford.edu:8080/checker", body:"{'expressions':'x>2', 'bounds',''}"}
sendRequest :: API_Requests  -> Effect Unit --probably not the right types
sendRequest info = launchAff_ do
    
    result <- AX.request (AX.defaultRequest { url = info.url, method = Left POST, responseFormat = ResponseFormat.json, headers = [RequestHeader "Content-Type" "application/json"], content = (Just(RequestBody.string  (JSON.writeJSON info.body)))})
    case result of
        Left err -> log $ "POST http://blum.cs.haverford.edu:8080/checker response failed to decode: " <> AX.printError err
        Right response -> log $ "POST http://blum.cs.haverford.edu:8080/checker response: " <> stringify response.body

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