import styled from 'styled-components';
export const Header = styled.div`
padding-top: 20px;
    border-bottom: 1px solid #ddd;



`

export const Header__inner = styled.div`
max-width: 1230px;
    padding-right: 15px;
    padding-left: 15px;
    margin-right: auto;
    margin-left: auto;



`

export const Header_utilities = styled.div`
display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 40px;



`

export const Header_utilities__logo = styled.div`
width: 150px;



`

export const Header_utilities__btn = styled.div`
width: auto;
    padding: 10px 20px;
    box-shadow: none;



`

export const Header_nav = styled.div`
display: flex;
    justify-content: space-around;



`

export const Header_nav__link = styled.div`
position: relative;
    display: block;
    padding: 15px 5px;
    border-bottom: 4px solid transparent;
    color: #222;
    text-decoration: none;
    transition: .25s;

&:focus {
border-bottom-color: #e25c00;
}                

&:hover {
border-bottom-color: #e25c00;
}                


&::after {
content: '';
    position: absolute;
    top: 50%;
    right: 0;
    width: 1px;
    height: 20px;
    background-color: #ddd;
    transform: translateY(-50%);
}


`

export const Header_nav__item = styled.div`
flex-grow: 1;
    text-align: center;



&:last_child {
${Header_nav__link}::after{
    content: none;
}
}

`
