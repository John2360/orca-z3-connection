module Z3 where

import Prelude
import Data.Maybe
import Data.Map
import Data.Either (Either(..))
import Affjax as AX
import Affjax.ResponseFormat as ResponseFormat
import Data.Argonaut.Core (stringify, fromString, Json)
import Effect.Class.Console (log)

import Effect (Effect)
import Effect.Aff (Aff, launchAff_)
import Effect.Aff.Compat (EffectFnAff, fromEffectFnAff)

import Affjax.RequestBody as RequestBody

type API_Requests = {
    url :: String,
    body :: String
}

--sample = {url:"http://blum.cs.haverford.edu:8080/checker", body:"{'expressions':'1'}"}
sendRequest :: API_Requests -> Effect Unit --probably not the right types
sendRequest info = launchAff_ do 
    result2 <- AX.post ResponseFormat.json info.url (Just (RequestBody.json (fromString info.body)))
    case result2 of
        Left err -> log $ "POST " <> info.url <> "; response failed to decode: " <> AX.printError err
        Right response -> log $ "POST " <> info.url <> "; response: " <> stringify response.body