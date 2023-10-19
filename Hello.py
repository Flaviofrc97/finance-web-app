# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Ola! Bem-vindo! 👋")

    st.markdown(
        """
        Esta é uma calculadora simples de amortização de empréstimos desenvolvida em Python com o uso do Streamlit 
        para criar uma interface de usuário amigável. A calculadora permite que os usuários insiram informações sobre seu empréstimo, 
        como taxa de juros, valor do empréstimo, prazo e período de carência, e calcula o valor da amortização (PMT) com base nesses dados 💰.
    """
    )

    st.markdown(
        """
        Sinta-se à vontade para contribuir para este projeto. Você pode relatar problemas,
          enviar solicitações de pull ou propor melhorias. Toda ajuda é bem-vinda! 🚀

          [github](https://github.com/Flaviofrc97/finance-web-app)
    """
    )


if __name__ == "__main__":
    run()
