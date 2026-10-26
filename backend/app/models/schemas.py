from typing import List, Literal, Optional, Dict, Any, Union
from pydantic import BaseModel, Field

class FoodAnalyzeRequest(BaseModel):
    food: str = Field(..., description="The food item name to analyze, e.g. 'Milk' or 'Turmeric'")

class SourceItem(BaseModel):
    name: str
    url: str

class GlobalProductInfo(BaseModel):
    brand: Optional[str] = ""
    countries: Optional[str] = ""
    ingredients: Optional[str] = ""
    barcode: Optional[str] = ""
    nutritionGrade: Optional[str] = ""
    nutritionPer100g: Dict[str, Any] = Field(default_factory=dict)
    url: str

class WebFoodInformation(BaseModel):
    title: str
    summary: str
    url: str

class NutritionInformation(BaseModel):
    source: str
    dataType: Optional[str] = None
    per100g: Dict[str, Any] = Field(default_factory=dict)
    url: str

class FoodAnalyzeSuccessResponse(BaseModel):
    isFood: Literal[True] = True
    classification: str = "food"
    foodName: str
    category: Optional[str] = "General Food"
    adulterants: List[str] = []
    whyAdulterated: str = ""
    healthRisks: List[str] = []
    testMethod: str = ""
    testProcedure: Optional[str] = ""
    observation: str = ""
    safeTips: List[str] = []
    storageTips: List[str] = []
    sources: List[SourceItem] = []
    dataSource: Optional[str] = None
    productInfo: Optional[GlobalProductInfo] = None
    webInformation: Optional[WebFoodInformation] = None
    nutritionInformation: Optional[NutritionInformation] = None
    disclaimer: Optional[str] = "This is only a preliminary awareness check. Laboratory testing is required for confirmation. Do not consume or handle suspicious substances during testing."

class NonFoodResponse(BaseModel):
    isFood: Literal[False] = False
    classification: Literal["non_food", "uncertain"] = "non_food"
    foodName: str
    message: str = "This is not a food item."
    suggestion: Optional[str] = "Please enter a food item such as: Milk, Rice, Turmeric, Honey, Sugar or Edible Oil."
    sources: List[SourceItem] = []

class ChatMessage(BaseModel):
    role: str # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    foodContext: Optional[str] = None
    history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    reply: str
    isFoodRelated: bool = True
    suggestedFollowUps: Optional[List[str]] = []
    sources: Optional[List[SourceItem]] = []

class FeedbackCreateRequest(BaseModel):
    name: str
    location: str
    rating: int = 5
    comments: str

class FeedbackResponse(BaseModel):
    status: str
    message: str
