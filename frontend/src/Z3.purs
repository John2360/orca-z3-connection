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

type API_Requests = {
    url :: String,
    body :: String
}

--sample = {url:"http://blum.cs.haverford.edu:8080/checker", body:"{'expressions':'x>2', 'bounds',''}"}
sendRequest :: API_Requests -> Effect Unit --probably not the right types
sendRequest info = launchAff_ do 
    result <- AX.request (AX.defaultRequest { url = "http://blum.cs.haverford.edu:8080/checker", method = Left POST, responseFormat = ResponseFormat.json, headers = [RequestHeader "Content-Type" "application/json"], content = (Just(RequestBody.json (fromString "{'expressions':'x>2'}")))})
    case result of
        Left err -> log $ "POST http://blum.cs.haverford.edu:8080/checker response failed to decode: " <> AX.printError err
        Right response -> log $ "POST http://blum.cs.haverford.edu:8080/checker response: " <> stringify response.body
        